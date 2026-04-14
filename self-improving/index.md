# Self-Improving Memory Index

| File | 用途 | Last Updated |
|------|------|--------------|
| heartbeat-state.md | 心跳状态追踪（状态机、最近错误、待处理动作） | 2026-04-14 |
| heartbeat-rules.md | 心跳完整规则（SENSE→THINK→EXECUTE→EVALUATE→LEARN闭环 + Phase3探索模式） | 2026-04-14 |
| exploration-log.md | 探索模式记录（试探过程/结果/升级记录） | 2026-04-14 |
| execution-log.md | 每次任务的完整执行记录（自校正素材） | 2026-04-14 |
| experience-index.md | 经验库索引（按领域/任务类型组织） | 2026-04-14 |
| **phase4-integration.md** | **Phase 4 综合集成体系（知识层次/分解引擎/调度规范）** | **2026-04-14** |
| **SKILL-MAP.md** | **所有已装 Skill 能力地图（19个skill与领域绑定矩阵）** | **2026-04-14** |
| memory.md | 长期偏好、模式、规则（HOT tier） | — |
| corrections.md | 执行错误教训记录 | — |
| domains/ | 各领域执行模式沉淀 | — |
| projects/ | 项目级记忆（按需创建） | — |
| archive/ | 历史归档 | — |

---

## Phase 4 综合集成 — 知识层次体系

```
Layer 1 原始记录   → execution-log, exploration-log, memory/YYYY-MM-DD
Layer 2 领域模式   → self-improving/domains/[领域].md
Layer 3 高层智慧   → MEMORY.md, SOUL.md, self-improving/memory.md
```

## Phase 4 任务分解引擎

```
复杂任务触发 → 分解为子任务树 → 判断并行/串行 → subagent执行 → 整合结果
```

---

## 快速规则
- 置信度 ≥ 0.85 → 直接执行
- 置信度 0.70-0.84 → 谨慎执行
- 置信度 < 0.70 → 探索模式
- 2+ 领域任务 → 引用 SKILL-MAP × 领域绑定矩阵
- 3+ 步骤任务 → 触发分解引擎，写入 domains/general.md
