# Self-Improving Memory Index

| File | 用途 | Last Updated |
|------|------|--------------|
| heartbeat-state.md | 心跳状态追踪（状态机、最近错误、待处理动作） | 2026-04-14 |
| heartbeat-rules.md | 心跳完整规则（SENSE→THINK→EXECUTE→EVALUATE→LEARN闭环 + Phase3探索模式） | 2026-04-14 |
| exploration-log.md | 探索模式记录（试探过程/结果/升级记录） | 2026-04-14 |
| execution-log.md | 每次任务的完整执行记录（自校正素材） | 2026-04-14 |
| experience-index.md | 经验库索引（按领域/任务类型组织） | 2026-04-14 |
| memory.md | 长期偏好、模式、规则（HOT tier） | — |
| corrections.md | 执行错误教训记录 | — |
| domains/ | 各领域执行模式沉淀（按需创建） | — |
| projects/ | 项目级记忆（按需创建） | — |
| archive/ | 历史归档 | — |

## Phase 3 核心机制

```
未知任务 / 置信度 < 0.7
        ↓
  EXPLORING 状态
        ↓
  小范围试探（最多3次）
        ↓
  试探成功 → 置信度+0.2 → 升级为正常执行
  试探失败 → 记录教训 → 换方法或交用户
        ↓
  3次全成功 → 沉淀为领域经验，更新 experience-index
```

## 快速规则
- 置信度 ≥ 0.85 → 直接执行
- 置信度 0.70-0.84 → 谨慎执行
- 置信度 < 0.70 → 探索模式
- 同一任务最多 3 次试探，失败交用户
