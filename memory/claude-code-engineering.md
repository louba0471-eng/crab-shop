# Claude Code 工程化实践报告（2026-04-09）

> 通过源码泄露仓库 `777genius/claude-code-source-code-full` 学习整理

---

## 一、工具系统（Tool System）

### 1.1 核心工厂模式 `buildTool()`

所有工具通过统一的 `buildTool()` 工厂创建，标准接口：

```typescript
export const MyTool = buildTool({
  name: 'MyTool',
  aliases: ['my_tool'],
  description: '工具描述',
  inputSchema: z.object({
    param: z.string(),
  }),
  async call(args, context, canUseTool, parentMessage, onProgress) {
    // 执行逻辑
    return { data: result, newMessages?: [...] }
  },
  async checkPermissions(input, context) {
    // 权限检查
    return { granted: boolean, reason?, prompt? }
  },
  isConcurrencySafe(input) { /* 能否并行 */ },
  isReadOnly(input) { /* 是否只读 */ },
  prompt(options) { /* 系统提示词贡献 */ },
  renderToolUseMessage(input, options) { /* 终端渲染-调用 */ },
  renderToolResultMessage(content, progressMessages, options) { /* 终端渲染-结果 */ },
})
```

### 1.2 工具目录结构（每个工具自包含）

```
src/tools/MyTool/
├── MyTool.ts(x)       # 主实现（Zod schema + call 方法）
├── UI.tsx            # 终端渲染（Ink React 组件）
├── prompt.ts         # 系统提示词贡献
├── utils.ts          # 工具函数
└── index.ts          # 导出
```

### 1.3 工具注册（tools.ts）

```typescript
// 直接导入（编译时包含）
import { AgentTool } from './tools/AgentTool/AgentTool.js'
import { BashTool } from './tools/BashTool/BashTool.js'

// 条件导入（feature flag 裁剪）
const SleepTool = feature('PROACTIVE') || feature('KAIROS')
  ? require('./tools/SleepTool/SleepTool.js').SleepTool
  : null

// 环境裁剪（员工版 vs 公开版）
const REPLTool = process.env.USER_TYPE === 'ant'
  ? require('./tools/REPLTool/REPLTool.js').REPLTool
  : null
```

**三大裁剪机制：**
1. `feature('FLAG_NAME')` — 构建时裁剪未启用特性
2. `process.env.USER_TYPE === 'ant'` — 员工专属功能
3. `require()` 延迟导入 — 惰性加载

### 1.4 工具分类（~40 个）

| 类别 | 工具数 | 代表工具 |
|------|--------|----------|
| 文件系统 | 7 | FileRead, FileWrite, FileEdit, Glob, Grep |
| Shell/执行 | 3 | Bash, PowerShell, REPL |
| Agent/编排 | 10 | Agent, SendMessage, TeamCreate, EnterPlanMode |
| 任务管理 | 6 | TaskCreate, TaskUpdate, TaskStop |
| Web | 2 | WebFetch, WebSearch |
| MCP | 5 | MCPTool, ListMcpResources, ToolSearch |
| 集成 | 2 | LSPTool, SkillTool |

### 1.5 权限模型

```typescript
// 权限检查流程
Tool → checkPermissions(input, context) → PermissionContext → handlers → user prompt

// 权限模式
type PermissionMode = 'default' | 'plan' | 'bypassPermissions' | 'auto'

// 权限规则（通配符匹配）
Bash(git *)           // 放行所有 git 命令
FileEdit(/src/*)     // 允许编辑 src/ 下所有文件
FileRead(*)           // 允许读取任意文件
```

### 1.6 工具设计关键模式

**设备文件黑名单（FileReadTool）：**
```typescript
const BLOCKED_DEVICE_PATHS = new Set([
  '/dev/zero', '/dev/random', '/dev/stdin',
  '/dev/tty', '/dev/console', '/dev/stdout', '/dev/stderr',
])
// 读取前检查，防止进程阻塞
```

**权限预检查：**
```typescript
import { checkReadPermissionForTool, matchingRuleForInput } from '../../utils/permissions/filesystem.js'
```

---

## 二、命令系统（Command System）

### 2.1 三种命令类型

```typescript
type CommandType = 'prompt' | 'local' | 'local-jsx'

// PromptCommand — 发提示词给 LLM
const command = {
  type: 'prompt',
  name: 'review',
  description: 'AI 代码审查',
  allowedTools: ['Bash(git *)', 'FileRead(*)'],
  async getPromptForCommand(args, context) {
    return [{ type: 'text', text: '请审查以下代码...' }]
  },
}

// LocalCommand — 本地进程执行
const command = {
  type: 'local',
  name: 'cost',
  execute() { return plainTextResult }
}

// LocalJSXCommand — 本地执行但渲染 React
const command = {
  type: 'local-jsx',
  name: 'doctor',
  execute() { return <DoctorOutput /> }
}
```

### 2.2 命令注册（commands.ts）

```typescript
// 85+ 个命令，全部在 commands.ts 注册
// 同样使用 feature flag 条件加载
const proactive = feature('PROACTIVE')
  ? require('./commands/proactive.js').default
  : null

const voiceCommand = feature('VOICE_MODE')
  ? require('./commands/voice/index.js').default
  : null
```

### 2.3 核心命令分类

| 类别 | 命令 |
|------|------|
| Git | /commit, /diff, /branch, /pr_comments, /rewind |
| 代码质量 | /review, /security-review, /advisor, /bughunter |
| 会话管理 | /compact, /context, /resume, /session, /export |
| 配置 | /config, /permissions, /theme, /model, /effort |
| 记忆 | /memory, /add-dir, /files |
| MCP/插件 | /mcp, /plugin, /skills |
| 诊断 | /doctor, /status, /cost, /version |

---

## 三、QueryEngine（核心引擎）

### 3.1 位置与规模
- 文件：`src/QueryEngine.ts`（~46K 行）
- 这是 Claude Code 最大的单一文件

### 3.2 核心职责
```
QueryEngine
├── 流式响应处理（Streaming）
├── 工具调用循环（Tool Call Loop）
│   └── LLM 请求工具 → 执行 → 反馈结果 → 继续
├── 思维模式（Thinking with budget）
├── 重试逻辑（自动退避重试）
├── Token 计数（输入/输出/成本追踪）
└── 上下文管理（对话历史/上下文窗口）
```

### 3.3 API 调用流程
```
main.tsx (CLI 解析)
  → replLauncher.tsx (REPL 会话启动)
    → QueryEngine.ts (核心引擎)
      → src/services/api/ (Anthropic SDK 客户端)
        → Anthropic API (HTTP/流式)
      ← 工具响应
      → src/tools/{ToolName}/ (工具执行)
      ← 工具结果
      → 反馈给 API (继续循环)
```

---

## 四、状态管理

### 4.1 模式：React Context + AppState Store

```typescript
// 全局可变状态
src/state/AppStateStore.ts
├── conversation history
├── settings
└── runtime state

// React Context（通知、统计、FPS）
src/context/
├── NotificationContext
├── StatsContext
└── FPSContext

// 派生状态选择器
src/state/selectors.ts

// 状态变更观察者（副作用）
src/state/onChangeAppState.ts
```

### 4.2 State 更新模式
- 变更观察者触发副作用（side-effects）
- AppState 通过 context 注入工具上下文

---

## 五、UI 层（React + Ink）

### 5.1 技术栈
- **Ink**：React 的 terminal 渲染版本
- **Chalk**：终端颜色
- **React Compiler**：编译时优化重渲染

### 5.2 组件规模
- `src/components/`：~140 个 React 组件
- `src/hooks/`：~80 个 hooks
- `src/screens/`：全屏模式（REPL、Doctor、ResumeConversation）

### 5.3 屏幕系统
```typescript
// 三种全屏模式
REPL.tsx              // 主交互界面（默认）
Doctor.tsx            // 环境诊断
ResumeConversation.tsx // 会话恢复
```

---

## 六、内存系统

### 6.1 位置：`src/memdir/`

### 6.2 记忆文件检测
```typescript
import { isAutoMemFile } from '../../utils/memoryFileDetection.js'
```

### 6.3 相关命令
- `/memory` — 管理 CLAUDE.md 持久记忆
- `/compact` — 压缩对话上下文
- 记忆新鲜度：`memoryFreshnessNote`

---

## 七、MCP（Model Context Protocol）

### 7.1 双重角色
- **MCP Client**：消费外部 MCP 服务器工具
- **MCP Server**：通过 `src/entrypoints/mcp.ts` 暴露自身工具

### 7.2 关键能力
- 工具发现（Tool discovery）
- 动态工具加载（`ToolSearchTool`）
- 资源浏览（Resources browsing）
- 认证流程（`McpAuthTool`）

---

## 八、Bridge 系统（IDE 集成）

### 8.1 架构
```
IDE Extension (VS Code/JetBrains)
        ↕  JWT 双向通信
Bridge Layer (src/bridge/)
        ↕
Claude Code Core (QueryEngine + Tools)
```

### 8.2 核心文件
| 文件 | 职责 |
|------|------|
| `bridgeMain.ts` | 双向通道主循环 |
| `bridgeMessaging.ts` | 消息协议（序列化/反序列化）|
| `bridgePermissionCallbacks.ts` | 权限提示路由到 IDE |
| `bridgeApi.ts` | 暴露给 IDE 的 API |
| `jwtUtils.ts` | CLI ↔ IDE JWT 认证 |

### 8.3 Feature Flag
`BRIDGE_MODE` — 非 IDE 构建版本会被裁剪掉

---

## 九、技能系统（Skills）

### 9.1 位置：`src/skills/`

### 9.2 结构
| 组件 | 位置 |
|------|------|
| 内置技能 | `src/skills/bundled/` |
| 技能加载器 | `src/skills/loadSkillsDir.ts` |
| MCP 技能构建器 | `src/skills/mcpSkillBuilders.ts` |

### 9.3 内置技能（16 个）
`batch`、`claudeApi`、`claudeInChrome`、`debug`、`keybindings`、`loop` 等

---

## 十、任务系统（Tasks）

### 10.1 后台任务管理
```
TaskCreateTool   → 创建后台任务
TaskUpdateTool   → 更新任务状态
TaskListTool     → 列出所有任务
TaskOutputTool   → 获取任务输出
TaskStopTool     → 停止任务
```

### 10.2 任务状态
- 运行中 / 完成 / 失败 / 停止

---

## 十一、关键工程化设计模式

### 11.1 特性开关（Feature Flags）
```typescript
// 构建时裁剪
import { feature } from 'bun:bundle'

if (feature('VOICE_MODE')) {
  // 未启用则整个代码块被剥离
}

// 条件注册
const tool = feature('SOME_FLAG') ? ToolA : ToolB
```

### 11.2 惰性加载
```typescript
// 重模块延迟到首次使用时导入
const { OpenTelemetry } = await import('./heavy-module.js')
```

### 11.3 ESM 规范
```typescript
// Bun 约定：所有导入使用 .js 扩展名（实际是 .ts 文件）
import { something } from './utils.js'  // 实际导入 utils.ts
```

### 11.4 双轨 User Type
```typescript
// Anthropic 员工版 vs 公开版
if (process.env.USER_TYPE === 'ant') {
  // 员工专属功能
}
```

### 11.5 Zod v4 数据验证
```typescript
inputSchema: z.object({
  param: z.string(),
  optional: z.string().optional(),
  nested: z.object({ key: z.string() }),
})
```

### 11.6 统一错误处理
```typescript
// 设备文件黑名单检查
if (isBlockedDevicePath(filePath)) {
  throw new Error('Cannot read blocked device')
}

//ENOENT 处理
import { isENOENT } from '../../utils/errors.js'
```

### 11.7 遥测与可观测性
```typescript
// OpenTelemetry 分布式追踪
// GrowthBook A/B 测试
// 自定义事件追踪
import { logEvent } from '../../services/analytics/index.js'
```

---

## 十二、可复用的设计思想

1. **工具即模块**：每个能力（工具/命令/技能）自包含，有明确的输入、输出、权限、渲染
2. **注册表模式**：所有工具在 `tools.ts` 注册，所有命令在 `commands.ts` 注册
3. **工厂模式**：`buildTool()` 统一构建流程，保证一致性
4. **Feature Flag 裁剪**：不同版本用同一套代码，通过 flag 控制功能取舍
5. **Pipeline 架构**：Input → Parse → Execute → Loop → Render，职责清晰
6. **权限分级**：default / plan / bypass / auto，灵活的安全控制
7. **惰性加载**：重模块按需导入，加快启动速度
8. **React + Ink**：用 Web 开发模式做终端 UI，组件化程度高

---

*报告生成时间：2026-04-09*
*来源：Claude Code 源码泄露仓库（777genius/claude-code-source-code-full）*
