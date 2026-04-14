# 经验库索引

> 按领域和任务类型组织的经验检索入口

| 领域 | 文件 | 描述 |
|------|------|------|
| feishu | domains/feishu.md | 飞书日历、消息、文档、多维表格 |
| web | domains/web.md | 搜索、网页抓取 |
| code | domains/code.md | 代码执行、Claude Code |
| system | domains/system.md | 系统操作、文件管理 |
| enterprise | domains/enterprise.md | 企业AI诊断、数字化转型（Phase 3 探索验证） |
| general | domains/general.md | 通用模式、任务分解模板、降级策略（Phase 4） |

## 按任务类型索引

| 任务类型 | 经验摘要 |
|----------|----------|
| 搜索信息 | 见 domains/web.md |
| 创建文档 | 见 domains/doc.md |
| 管理日历 | 见 domains/feishu.md |
| 发送消息 | 见 domains/feishu.md |
| 执行代码 | 见 domains/code.md |
| 文件处理 | 见 domains/system.md |
| 企业AI诊断 | 见 domains/enterprise.md（Phase 3 探索验证：置信度 0.6→0.8，使用 enterprise-ai-diagnosis skill） |

| 任务 | 成功率 | 推荐方法 |
|------|--------|----------|
| 架构升级/系统改造 | 100% (1次) | 先理解原架构，再设计新架构，最后写入文件 + commit |
| 系统状态检查 | 100% (1次) | git log + 状态验证，快速执行 |
| Phase 2 自校正验证 | 100% (1次) | 完整走 SENSE→THINK→EXECUTE→EVALUATE→LEARN 5步闭环，THINK 查经验库，LEARN 写记录 |

## 失败模式记录

| 任务类型 | 常见失败原因 | 改进方向 |
|----------|-------------|----------|
| (待积累) | — | — |

