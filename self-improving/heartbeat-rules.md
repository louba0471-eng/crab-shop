# Heartbeat Rules — 工程控制论闭环自校正版

> 基于《工程控制论》STR 架构：每次 heartbeat = SENSE → THINK → EXECUTE → EVALUATE → LEARN 闭环循环

## 核心状态机

Agent 在每次心跳时处于以下状态之一：

```
IDLE → PLANNING → EXECUTING → EVALUATING
                        ↓            ↓
                   ERROR_FATAL   LEARNED
                        ↓
                   RECOVERING → IDLE
```

**状态说明：**
- `IDLE`：待命，无待处理任务
- `PLANNING`：分析状态，制定执行计划
- `EXECUTING`：执行计划
- `EVALUATING`：评估执行结果，对比预期
- `LEARNED`：总结经验，更新记忆，回归 IDLE
- `ERROR_FATAL`：执行失败，进入恢复
- `RECOVERING`：执行降级策略/修复，回归 IDLE

---

## 完整心跳循环（每次必执行）

### STEP 1 — SENSE（感知）

检查以下维度，汇总系统当前状态：

1. **上次心跳时间**：从 `heartbeat-state.md` 读取 `last_heartbeat_started_at`
2. **待处理任务**：检查是否有未完成的邮件/日历/提醒
3. **记忆热点**：读取 `self-improving/memory.md` 的 HOT tier（本次会话新写入的内容）
4. **上次执行结果**：从 `heartbeat-state.md` 读取 `last_outcome`
5. **最近异常**：检查 `heartbeat-state.md` 的 `recent_errors[]`
6. **时间上下文**：判断当前时段（早/午/晚/深夜）

> 如果距离上次心跳 <5 分钟且状态为 IDLE，直接返回 `HEARTBEAT_OK`（防止抖动）

---

### STEP 2 — THINK（决策）

基于感知结果 + 历史经验，判断本次心跳应该做什么：

**【自校正查询】先查经验库：**
- 读取 `self-improving/experience-index.md`，了解高频任务和已知模式
- 读取相关 `self-improving/domains/[领域].md`
- 如有匹配的历史经验 → 优先采用成功路径；如曾失败 → 跳过该方法或换降级策略

**判断优先级（从高到低）：**

1. **紧急异常处理**：如果 `recent_errors` 非空 → 状态=RECOVERING，执行错误修复
2. **待发消息**：检查 `heartbeat-state.md` 的 `pending_actions[]` → 执行发送
3. **日历提醒**：未来 2 小时内有日历事件 → 发出提醒
4. **记忆维护**：如果上次心跳距今 > 8 小时 → 执行记忆整理（见下方）
5. **常规检查**：如果距上次同类检查超过阈值 → 检查邮件/天气等
6. **无事发生**：以上都没有 → 状态=IDLE，返回 `HEARTBEAT_OK`

**经验引导规则：**
- 如果当前任务类型在 `experience-index.md` 的"失败模式记录"中有案底 → 先检查那次失败的原因是否已消除
- 如果是未知任务类型 → 触发"探索模式"，小范围试错

---

### STEP 3 — EXECUTE（执行）

根据决策结果执行对应动作：

**动作库（按类型）：**

#### A. 记忆整理（Memory Maintenance）
- 扫描 `memory/` 目录，找出最近 48 小时内的日记
- 提炼：决策、教训、待办
- 更新 `MEMORY.md` 的 relevant sections
- 写回 `heartbeat-state.md`：`last_memory_maintenance_at`

#### B. 错误恢复（Error Recovery）
- 读取 `recent_errors[]`
- 对每条错误尝试自动修复（重试 / 降级 / 记录无法修复）
- 执行完毕后清空 `recent_errors[]`
- 写经验到 `self-improving/corrections.md`

#### C. 日历检查（Calendar Check）
- 查询未来 2 小时日历事件
- 有事件 → 发提醒给用户，返回事件摘要
- 无事件 → 继续

#### D. 邮件检查（Email Check）
- 检查未读邮件（如果配置了邮件工具）
- 高优先级邮件（发件人匹配 / 关键词匹配）→ 提醒用户
- 写回 `heartbeat-state.md`：`last_email_check_at`

#### E. 定时任务执行（Scheduled Task）
- 读取 `heartbeat-state.md` 的 `scheduled_tasks[]`
- 执行到达触发时间的任务
- 更新任务状态

---

### STEP 4 — EVALUATE（评估）

执行完毕后，对本次心跳的**所有执行结果**进行评估：

**评估维度：**

1. **执行是否成功**：每个动作逐一核对
2. **是否产生新错误**：记录到 `recent_errors[]`
3. **是否有意外收获**：执行结果超出预期 → 写入 `self-improving/memory.md` PATTERNS
4. **用户是否有反馈**：检查是否有用户新消息（本次心跳期间）

**评估结论写入 `heartbeat-state.md` 的 `last_outcome`：**
```markdown
last_outcome: |
  timestamp: ISO8601
  state_before: IDLE
  actions_taken: [动作列表]
  errors_encountered: [错误列表]
  assessment: success | partial | failed
  unexpected_results: [意外结果]
```

---

### STEP 5 — LEARN（学习）

基于评估结果，更新记忆、经验和策略：

**【自校正写入】每次执行必须记录：**
- 将本次任务写入 `self-improving/execution-log.md`（按格式：任务类型、时间戳、结果、过程、教训）
- 更新 `self-improving/experience-index.md`：
  - 成功 → 在"高频任务优化路径"表追加一行（任务/成功率/推荐方法）
  - 失败 → 在"失败模式记录"表追加一行（任务/失败原因/改进方向）

**经验更新规则：**
- 如果某任务类型成功率 > 80%，下次优先用同一方法
- 如果某任务类型成功率 < 50%，标记为"探索模式"候选
- 同一失败原因出现 2 次以上 → 写入 `domains/[领域].md` 的"常见错误"，作为预防知识

**分流更新：**
- 成功执行 → 追加到 `execution-log.md`，更新 `experience-index.md`
- 部分成功 → 同上，但额外写教训到 `corrections.md`
- 失败 → 写错误详情到 `recent_errors[]`，教训写入 `corrections.md`，更新"失败模式记录"
- 新模式/新教训 → 同步更新相关 `domains/[领域].md`

---

## 状态转移规则

```
任意状态 + 紧急异常 → ERROR_FATAL → RECOVERING → IDLE
IDLE + 有待处理任务 → PLANNING
PLANNING + 计划制定完成 → EXECUTING
EXECUTING + 所有动作完成 → EVALUATING
EVALUATING + 评估完成 → LEARNED → IDLE
RECOVERING + 修复尝试3次仍失败 → IDLE（记录待办，不再自动重试）
```

---

## 稳定性保障（工程控制论第三章）

1. **心跳间隔保护**：两次心跳至少间隔 5 分钟（除非有紧急异常）
2. **最大执行时间**：单个动作超时 30 秒，强杀并记录错误
3. **错误计数上限**：`recent_errors[]` 超过 5 条 → 停止自动执行，发通知
4. **降级链**：如果方法A失败 → 自动换方法B → 方法C（最多3级）

---

## 不确定性处理（工程控制论第四章）

1. **置信度 < 0.7 的判断**：不自动执行，先记录到 `pending_review[]`，等用户确认
2. **多源信息冲突**：交叉验证，少数服从多数，无法判断 → 询问用户
3. **未知任务类型**：触发"探索模式"——小范围试错，记录结果，扩展到完整执行

---

## 执行记录规范

每次心跳结束，必须更新 `heartbeat-state.md`：

```markdown
last_heartbeat_started_at: ISO8601
last_heartbeat_ended_at: ISO8601
last_outcome: (见上方格式)
last_state: IDLE | PLANNING | ...
last_actions_summary: 简短描述
recent_errors: []  # 最多保留5条，自动清理超过24小时的旧错误
pending_actions: []  # 待执行的延迟动作
last_email_check_at: ISO8601 | null
last_calendar_check_at: ISO8601 | null
last_memory_maintenance_at: ISO8601 | null
next_scheduled_tasks: []  # 未来定时任务
```

---

## 快速路径（优化）

- 无异常 + 无待处理 + 常规检查未到期 → 直接 `HEARTBEAT_OK`，不执行完整5步
- 但**每次心跳必须写** `last_heartbeat_started_at` 和 `last_heartbeat_ended_at`（用于判断是否需要执行记忆整理）
- **每10次心跳强制执行一次完整5步**（防止快速路径导致长期不维护）
