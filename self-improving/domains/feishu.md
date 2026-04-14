# 飞书（Feishu）领域经验

> 飞书日历、消息、文档、多维表格、云空间相关任务经验

## 日历（Calendar）

### 创建日程
**成功率：** 高  
**推荐流程：**
1. 先查主日历 `feishu_calendar_calendar primary`
2. 创建时必传 `user_open_id`（从消息上下文 SenderId 获取，格式 ou_xxx）
3. 时间用 ISO 8601 / RFC 3339，含时区，如 `2024-01-01T00:00:00+08:00`
4. 默认生成飞书视频会议，首次添加参会人时自动创建

**常见错误：**
- 未传 `user_open_id` → 日程只出现在应用日历，用户看不到
- 时区遗漏 → 时间错乱

### 查询日程
- `list` 用 `instance_view` 接口，自动展开重复日程
- 时间区间不超过 40 天，上限 1000 条

### 忙闲查询
- `feishu_calendar_freebusy`：批量查 1-10 用户主日历
- 时间区间无明确限制，但建议单次不超过 7 天

---

## 消息（IM）

### 发送消息
**注意：** 仅用户明确要求"以我身份发送"时使用 `feishu_im_user_message`  
**正常情况：** 直接用 message 系统工具

发送前必须确认：
1. 发送对象（chat_id 群聊 / open_id 私聊）
2. 消息内容

### 搜索消息
- `feishu_im_user_search_messages`：跨会话搜索
- 至少提供一个过滤条件
- `relative_time` 和 `start_time/end_time` 不能同时用

### 下载资源
- 当前对话中的图片/文件 → `feishu_im_bot_image`（机器人身份，无需授权）
- 用户消息列表中获取的资源 → `feishu_im_user_fetch_resource`（需用户 OAuth）

---

## 文档（Docs）

### 创建文档
- 使用 `feishu_create_doc` 从 Markdown 创建
- 支持创建到文件夹（folder_token）或知识库（wiki_space）

### 获取文档
- `feishu_fetch_doc`：返回 Markdown，支持大文档分页
- 图片/文件需用 `feishu_doc_media insert` 插入

### 更新文档
- `feishu_update_doc`：支持 overwrite / append / replace_range 等模式
- 插入图片用 `<image url="..."/>` 语法

---

## 多维表格（Bitable）

### 创建表
- 明确字段需求时，在 `create` 时通过 `fields` 数组一次性定义所有字段（减少 API 调用）
- 探索式场景：先用默认表，再用 `feishu_bitable_app_table_field` 逐个添加

### 记录操作
- `create` 用 `fields` 对象（单条）
- `batch_create` 用 `records` 数组（批量，最多 500 条）
- 日期字段：传毫秒时间戳
- 人员字段：`[{id: 'ou_xxx'}]`

---

## 搜索（Search）

### 搜索用户
- `feishu_search_user`：按姓名/手机/邮箱搜索
- 返回 open_id、姓名、部门

### 搜索文档/Wiki
- `feishu_search_doc_wiki`：统一搜索云空间和知识库
- 支持按类型、创建者、时间过滤
- 结果含标题摘要高亮

---

## 经验教训

1. **user_open_id 是高频坑**：日历创建必须传，其他场景注意上下文
2. **消息发送前必须确认**：安全约束，不能自动发
3. **下载资源分流**：当前对话用 bot_image，其他用 user_fetch_resource
