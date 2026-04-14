# Code 领域经验

> 代码执行、Claude Code、技术任务经验

## Claude Code

### 使用场景
- 复杂代码修改/重构
- 需要多轮迭代的编码任务
- 代码审查和优化

### 调用方式
- `sessions_spawn runtime="acp" agentId="..."`
- `mode="session"` 持久化线程
- `mode="run"` 单次执行

---

## 本地执行

### exec 工具
- 默认工作目录：`/Users/yu/.openclaw/workspace`
- 支持后台执行：`background: true` 或 `yieldMs`
- PTY 模式：`pty: true`（用于需要终端的 CLI）

### 安全约束
- 安装操作必须验证 OS/平台兼容性
- 破坏性命令（rm/trunc）要先问
- `/approve` 是用户确认命令，不是执行命令

---

## 经验教训

1. **复杂任务用 subagent** 而不是在主会话循环
2. **需要 TTY 的命令**（vim/less/交互式CLI）→ `pty: true`
3. **后台任务** → 用 `yieldMs` 等待一段时间，或 `background: true`
4. **安装前必验证平台** → macOS/Linux 不兼容教训已有先例
