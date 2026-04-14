# Corrections Log

> 执行中的错误、教训、自动校正记录

---

## 2026-04-14 工程控制论心跳改造

### 改造背景
- 原有 HEARTBEAT.md 逻辑极简：仅检查 self-improving/ 是否有变更，无实际执行逻辑
- 参照钱学森《工程控制论》设计闭环自校正心跳架构

### 改造内容
- 新建 heartbeat-rules.md：SENSE→THINK→EXECUTE→EVALUATE→LEARN 完整闭环
- 新建 heartbeat-state.md：状态机追踪、错误管理、定时任务管理
- 更新 HEARTBEAT.md：指向新规则
- 更新 index.md：更新索引

### 设计原则
1. 状态机：IDLE / PLANNING / EXECUTING / EVALUATING / ERROR_FATAL / RECOVERING
2. 闭环反馈：每次执行结果影响下次决策
3. 稳定性：心跳间隔保护（≥5分钟）、最大执行时间（30秒/动作）
4. 鲁棒性：错误计数阈值（>5条停自动执行）、降级策略链
5. 不确定性：置信度<0.7不自动执行，探索模式处理未知任务
