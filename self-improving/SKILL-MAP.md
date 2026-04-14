# Skill 能力地图（Skill Map）

> Phase 4 综合集成核心组件。记录所有已装 skill 的能力、适用场景、与领域知识的绑定关系。

---

## Skill 总览

| Skill | 一句话能力 | 适用任务类型 |
|-------|-----------|------------|
| **飞书系列** | | |
| feishu-calendar | 日历管理/日程创建/忙闲查询 | 日程管理、会议安排 |
| feishu-im-read | 消息读取/搜索/下载资源 | 聊天记录查询 |
| feishu-task | 任务管理/清单/子任务 | 任务追踪 |
| feishu-bitable | 多维表格管理 | 数据管理 |
| feishu-create-doc | 云文档创建 | 文档生成 |
| feishu-update-doc | 云文档更新 | 文档编辑 |
| feishu-fetch-doc | 云文档读取 | 文档读取 |
| feishu-search-doc-wiki | 文档/Wiki搜索 | 搜索飞书内容 |
| feishu-sheet | 电子表格管理 | 表格处理 |
| **搜索/信息** | | |
| multi-search-engine | 17引擎搜索（8国内+9海外） | 深度搜索、网络信息 |
| web_search | Tavily结构化搜索 | 快速信息获取 |
| web_fetch | 网页内容提取 | 深度阅读网页 |
| **文档生成** | | |
| minimax-docx (yh-minimax-docx) | Word文档创建/编辑/格式化 | 报告/合同/方案 |
| pptx-generator | PPT生成 | 演示文稿 |
| minimax-xlsx | Excel/XLSX表格 | 数据分析/报表 |
| **内容创作** | | |
| wechat-article-publisher | 微信公众号发布 | 微信内容运营 |
| **AI/自动化** | | |
| enterprise-ai-diagnosis | 企业AI诊断/ROI计算 | 企业AI规划 |
| agent-browser | 浏览器自动化 | 网页操作/抓取 |
| claude-code-code-simplifier | 代码审查/简化 | 代码质量优化 |
| lossless-claw | 对话蒸馏/记忆提取 | 记忆管理 |
| **系统工具** | | |
| self-improving | 自我改进/记忆管理 | 心跳/自校正 |
| skill-creator-agent | Skill创建/编辑/打包 | 技能开发 |
| find-skills-skill | 搜索安装新skill | 技能扩展 |
| ralph-mode | 自主开发循环/迭代 | 复杂编码任务 |
| **垂直领域** | | |
| ima-skill | 笔记/知识库管理 | 个人知识管理 |
| douyin-video | 抖音视频下载 | 视频内容获取 |
| ui-ux-pro-max | UI/UX设计/实现 | 界面设计/前端 |

---

## Skill × 领域绑定矩阵

| 任务/场景 | 推荐 Skill | 绑定领域 |
|-----------|-----------|---------|
| 飞书日历创建 | feishu-calendar | domains/feishu.md |
| 飞书消息搜索 | feishu-im-read | domains/feishu.md |
| 飞书多维表格 | feishu-bitable | domains/feishu.md |
| 飞书文档创建 | feishu-create-doc | domains/feishu.md |
| 网络信息搜索 | multi-search-engine / web_search | domains/web.md |
| 网页深度阅读 | web_fetch | domains/web.md |
| Word报告撰写 | minimax-docx | domains/doc.md（建议新建） |
| PPT制作 | pptx-generator | domains/doc.md |
| Excel数据分析 | minimax-xlsx | domains/doc.md |
| 微信文章发布 | wechat-article-publisher | domains/media.md（建议新建） |
| 企业AI诊断 | enterprise-ai-diagnosis | domains/enterprise.md |
| 浏览器自动化 | agent-browser | domains/web.md |
| 代码审查优化 | claude-code-code-simplifier | domains/code.md |
| 复杂编码任务 | ralph-mode | domains/code.md |
| 记忆蒸馏管理 | lossless-claw | system |
| Skill开发 | skill-creator-agent | domains/code.md |
| 新技能发现 | find-skills-skill | system |
| 笔记/知识库 | ima-skill | 建议合并到 domains/enterprise.md 或新建 domains/knowledge.md |
| UI/UX设计 | ui-ux-pro-max | domains/design.md（建议新建） |
| 抖音视频处理 | douyin-video | domains/media.md |

---

## 复杂任务分解参考

当用户任务涉及多个 skill 时，按以下顺序引用 SKILL-MAP：

```
Step 1 — 识别所需 Skill
  → 查本 SKILL-MAP 的"Skill 总览"表

Step 2 — 识别所需领域知识
  → 查"Skill × 领域绑定矩阵"

Step 3 — 判断并行/串行
  → 独立 skill 调用 → 并行执行（subagent）
  → 有依赖链 → 串行执行

Step 4 — 整合输出
  → 按分解计划合并结果
  → 写入 execution-log
```

---

## 待补充领域

- [ ] domains/doc.md — 文档创建/编辑领域（Word/PPT/Excel 通用模式）
- [ ] domains/media.md — 内容创作领域（微信/抖音/视频）
- [ ] domains/design.md — UI/UX设计领域
- [ ] domains/knowledge.md — 个人知识管理（ima-skill 相关）

---

*本文件由 Phase 4 综合集成体系自动维护，每次安装新 skill 后更新*
