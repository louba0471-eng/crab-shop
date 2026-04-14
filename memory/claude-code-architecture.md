# Claude Code 架构笔记（2026-04-09）

## 核心架构：Pipeline 模型

```
User Input → CLI Parser → Query Engine → LLM API → Tool Execution Loop → Terminal UI
```

**QueryEngine.ts** (~46K 行)：流式响应、工具调用循环、重试逻辑、思维模式、Token 计数、上下文管理
**Tool.ts** (~29K 行)：工具类型、`buildTool` 工厂、权限模型
**commands.ts** (~25K 行)：命令注册表、条件加载

## 工具系统

### 核心原则
- 每个工具是**自包含模块**，位于 `src/tools/<ToolName>/`
- 每个工具定义：输入 schema（Zod）、权限模型、执行逻辑、UI 组件
- 用 `buildTool()` 工厂模式统一构建

### 工具分类（~40 个）
| 类别 | 工具 |
|------|------|
| 文件系统 | FileRead, FileWrite, FileEdit, Glob, Grep, NotebookEdit, TodoWrite |
| Shell/执行 | Bash, PowerShell, REPL |
| Agent/编排 | Agent, SendMessage, TeamCreate, TeamDelete, EnterPlanMode, ExitPlanMode, EnterWorktree, ExitWorktree, Sleep, SyntheticOutput |
| 任务管理 | TaskCreate, TaskUpdate, TaskGet, TaskList, TaskOutput, TaskStop |
| Web | WebFetch, WebSearch |
| MCP | MCPTool, ListMcpResources, ReadMcpResource, McpAuth, ToolSearch |
| 集成 | LSPTool, SkillTool |
| 调度 | ScheduleCron, RemoteTrigger |
| 工具 | AskUserQuestion, Brief, Config |

### 权限模型
- `default`：潜在破坏性操作需用户确认
- `plan`：显示完整计划，一次性确认
- `bypassPermissions`：自动批准（危险）
- `auto`：ML 分类器决定

## 命令系统（~85 个 slash 命令）

| 类型 | 行为 | 示例 |
|------|------|------|
| PromptCommand | 向 LLM 发送格式化提示 | /review, /commit |
| LocalCommand | 进程内运行，返回纯文本 | /cost, /version |
| LocalJSXCommand | 进程内运行，返回 React JSX | /doctor, /install |

## UI 层

- **React + Ink**：React 写 terminal UI，组件化
- ~140 个组件，~80 个 hooks
- 设计系统组件在 `src/components/design-system/`
- 状态管理：React Context + 自定义 AppState Store

## 技术栈

- **运行时**：Bun（不是 Node.js）
- **CLI 解析**：Commander.js
- **数据验证**：Zod v4
- **终端颜色**：Chalk
- **遥测**：OpenTelemetry + GrowthBook A/B 测试
- **特性开关**：Bun bundle  dead-code elimination

## 重要设计模式

### buildTool 工厂
```typescript
export const MyTool = buildTool({
  name: 'MyTool',
  inputSchema: z.object({ param: z.string() }),
  async call(args, context, canUseTool, parentMessage, onProgress) {
    return { data: result, newMessages?: [...] }
  },
  async checkPermissions(input, context) { ... },
  isConcurrencySafe(input) { ... },
  isReadOnly(input) { ... },
  prompt(options) { ... },
  renderToolUseMessage(input, options) { ... },
  renderToolResultMessage(content, progressMessages, options) { ... },
})
```

### 目录结构（每个工具）
```
src/tools/MyTool/
├── MyTool.ts        # 主实现
├── UI.tsx           # 终端渲染
├── prompt.ts        # 系统提示词贡献
└── utils.ts         # 工具函数
```

### API 调用流程
```
main.tsx → replLauncher.tsx → QueryEngine.ts → src/services/api/ → Anthropic API
                                              → src/tools/{ToolName}/ ← 工具执行
                                              ← 结果反馈 → 继续循环
```

## 关键文件（按行数）
| 文件 | 行数 | 内容 |
|------|------|------|
| QueryEngine.ts | ~46K | 流式、工具循环、重试、Token 计数 |
| Tool.ts | ~29K | 工具类型、buildTool、权限模型 |
| commands.ts | ~25K | 命令注册表、条件加载 |

## Feature Flags（构建时裁剪）
- `PROACTIVE`：主动 Agent 模式
- `BRIDGE_MODE`：IDE 桥接集成
- `VOICE_MODE`：语音输入/输出
- `COORDINATOR_MODE`：多 Agent 协调器
- `WORKFLOW_SCRIPTS`：工作流自动化脚本
