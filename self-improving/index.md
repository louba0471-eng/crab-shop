# Self-Improving Memory Index

| File | 用途 | Last Updated |
|------|------|--------------|
| heartbeat-state.md | 心跳状态追踪（状态机、最近错误、待处理动作） | 2026-04-14 |
| heartbeat-rules.md | 心跳完整规则（SENSE→THINK→EXECUTE→EVALUATE→LEARN闭环） | 2026-04-14 |
| memory.md | 长期偏好、模式、规则（HOT tier） | — |
| execution-log.md | 每次任务的完整执行记录（自校正素材） | — |
| experience-index.md | 经验库索引（按领域/任务类型组织） | — |
| domains/ | 各领域执行模式沉淀（按需创建） | — |
| projects/ | 项目级记忆（按需创建） | — |
| archive/ | 历史归档 | — |

## 核心概念（工程控制论闭环）

```
每次 heartbeat = STR 循环：
  SENSE → THINK → EXECUTE → EVALUATE → LEARN → IDLE
              ↑
        状态机：IDLE / PLANNING / EXECUTING / EVALUATING / ERROR_FATAL / RECOVERING
```

## 快速规则
- 两次心跳间隔 < 5 分钟 + 状态 IDLE → 直接 HEARTBEAT_OK
- 每 10 次心跳强制完整 5 步循环
- recent_errors > 5 条 → 停止自动执行，发通知
- 置信度 < 0.7 → 不自动执行，写入 pending_review
