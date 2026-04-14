# Heartbeat Rules — 工程控制论闭环自校正版 + Phase 3 自适应增强

> 基于《工程控制论》STR 架构：每次 heartbeat = SENSE → THINK → EXECUTE → EVALUATE → LEARN 闭环循环

---

## 核心状态机

```
IDLE → PLANNING → EXECUTING → EVALUATING → LEARNED → IDLE
                    ↓              ↓
               EXPLORING ←—————→ ERROR_FATAL
                    ↓
               RECOVERING → IDLE
```

**新增状态：**
- `EXPLORING`：识别到未知任务/新领域，进入小范围试错模式

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
7. **探索模式**：检查 `heartbeat-state.md` 的 `exploration_mode` 和 `exploration_tasks[]`

> 如果距离上次心跳 <5 分钟且状态为 IDLE 且无探索任务 → 直接返回 `HEARTBEAT_OK`

---

### STEP 2 — THINK（决策）

**【Phase 3 新增：置信度评分 + 新任务识别】**

#### 2.1 经验查询

- 读取 `self-improving/experience-index.md`
- 读取相关 `self-improving/domains/[领域].md`
- 匹配成功路径或识别失败规避

#### 2.2 新任务识别

判断当前是否遇到**新任务类型**：

**识别标准（满足任一即为新）：**
- 任务类型未在 `experience-index.md` 的任意表中出现
- 任务类型有记录但成功率 < 50%（说明现有方法不适用）
- 任务涉及**未建立领域文件**的新领域

**新任务识别 → 置 `exploration_mode: true`**

#### 2.3 置信度评分

**对每个判断输出置信度：**

| 场景 | 置信度基准 | 说明 |
|------|-----------|------|
| 经验库有成功路径 | ≥ 0.85 | 直接复用 |
| 经验库有失败记录但原因已消除 | 0.6-0.8 | 谨慎执行，监控结果 |
| 经验库无记录的新任务 | < 0.7 | **不自动执行**，进入探索模式 |
| 领域知识文件存在 | +0.1 | 有知识支撑 |
| 执行超时历史 | -0.2 | 稳定性存疑 |
| 多源信息一致 | +0.15 | 信息充分 |

**置信度 < 0.7 → 不自动执行，写入 `pending_review[]`，等用户确认**

#### 2.4 决策优先级

```
1. exploration_tasks[] 非空 → 进入 EXPLORING，执行探索任务
2. recent_errors 非空 → RECOVERING，错误修复
3. pending_review[] 非空 → 置信度不足，等待用户确认
4. pending_actions[] 非空 → 执行待发消息
5. 经验置信度 ≥ 0.7 → PLANNING，正常执行
6. 经验置信度 < 0.7 → EXPLORING，探索模式
```

---

### STEP 3 — EXECUTE（执行）

#### 正常执行模式

按决策执行动作库（见原有 A/B/C/D/E）。

#### **探索模式（EXPLORING）**

**触发条件：** 置信度 < 0.7 的新任务

**探索流程：**

```
STEP 3.1 — 界定范围
  将任务拆解为"最小可验证单元"
  限制：只执行 1 个工具调用 / 只读 1 个文件 / 只搜索 1 个信息点

STEP 3.2 — 执行试探
  执行最小单元，记录：
  - 用了什么工具/方法
  - 执行结果如何
  - 耗时/稳定性

STEP 3.3 — 结果评估
  成功 → 提炼为"试探成功方法"，可进入正常执行
  失败 → 记录失败原因，提炼为"试探失败教训"，可换方法重试

STEP 3.4 — 沉淀模式
  试探成功的方法 → 写入 `self-improving/exploration-log.md`
  并更新 `experience-index.md`：标注"试探阶段，待验证"
  
  试探失败的方法 → 写入 `exploration-log.md` 失败区，避免再用
```

**探索模式限制：**
- 最多连续 3 次试探（3 次都失败 → 记录"探索失败"，交用户处理）
- 每次试探完成后必须 LEARN，不允许跳过

---

### STEP 4 — EVALUATE（评估）

**正常模式：**
- 逐动作核对成功/失败
- 错误 → `recent_errors[]`
- 意外收获 → PATTERNS

**探索模式：**
- 每次试探后立即评估
- 记录到 `exploration-log.md` 的对应条目
- 成功 → 置信度提升（+0.2），可升级为正常执行
- 失败 → 置信度不变，探索其他方法或交用户

---

### STEP 5 — LEARN（学习）

**正常模式：** 同前版

**探索模式：**
- 试探结果 → `self-improving/exploration-log.md`
- 成功试探的模式 → 同步更新 `domains/[领域].md` 和 `experience-index.md`
- 失败试探的原因 → 写入 `recent_errors[]` 和 `corrections.md`

**经验更新规则补充：**
- 同一任务 3 次探索都成功 → 升级为"已知任务"，从 `exploration_tasks[]` 移除
- 探索成功率 > 80% → 从探索模式升级为正常任务
- 探索成功率 < 33% → 终止探索，标记为"困难任务"，交用户

---

## 状态转移规则（Phase 3 扩充）

```
IDLE + 有待处理任务 → PLANNING
IDLE + 新任务/置信度<0.7 → EXPLORING
PLANNING + 计划制定完成 → EXECUTING
EXECUTING + 所有动作完成 → EVALUATING
EVALUATING + 评估完成 → LEARNED → IDLE
EXPLORING + 试探成功 → EVALUATING → LEARNED → IDLE（若全部探索完成）
EXPLORING + 3次试探失败 → IDLE（记录探索失败，pending_review）
ERROR_FATAL → RECOVERING → IDLE
```

---

## 稳定性保障（Phase 3 扩充）

1. **心跳间隔保护**：两次心跳至少间隔 5 分钟
2. **最大执行时间**：单个动作超时 30 秒，强杀并记录错误
3. **错误计数上限**：`recent_errors[]` 超过 5 条 → 停止自动执行
4. **降级链**：方法A失败 → 方法B → 方法C（最多3级）
5. **探索限制**：同一任务最多 3 次试探探索，探索失败交用户

---

## 置信度速查表

执行前查这张表快速判断是否需要探索：

```
置信度 ≥ 0.85 → 直接执行（成功路径）
置信度 0.70-0.84 → 谨慎执行，边做边评估
置信度 < 0.70 → 探索模式，先小范围试探
```

---

## 快速路径（Phase 3 补充）

- 无异常 + 无待处理 + 常规检查未到期 + `exploration_tasks[]` 为空 → `HEARTBEAT_OK`
- **有探索任务时**：必须执行完所有 `exploration_tasks[]` 才能进入 IDLE
- 每 10 次心跳强制完整 5 步（含探索模式检查）
