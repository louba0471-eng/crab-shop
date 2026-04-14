# Self-Improving Heartbeat State

## 元数据
last_heartbeat_started_at: 2026-04-14T12:59:00+08:00
last_heartbeat_ended_at: 2026-04-14T12:59:30+08:00
last_heartbeat_count: 5
last_state: IDLE

## 上次执行结果
last_outcome: |
  timestamp: 2026-04-14T12:59:00+08:00
  state_before: IDLE
  actions_taken:
    - SENSE: 检查状态（无异常、无pending、距上次心跳99分钟）
    - THINK: 常规检查未到期（下一次日历检查14:59，邮件30min未到）
    - EXECUTE: 无紧急任务，快速路径结束
    - 发现明天07:30有"中新赛克沙龙|活动日"日程（南京），已记录
  errors_encountered: []
  assessment: success
  note: 发现未来日程：明日07:30 南京中新赛克沙龙活动日

## 异常管理
recent_errors: []

## 待处理动作
pending_actions: []

## 待用户确认（置信度不足）
pending_review: []

## 定时任务
next_scheduled_tasks:
  - calendar_event: "中新赛克沙龙 | 活动日"
    start: "2026-04-15T07:30:00+08:00"
    location: "南京市雨花台区宁双路19号云密城A栋15楼"
    note: "07:30工作人员到位, 14:00活动正式开始"

## 探索模式
exploration_mode: false
exploration_tasks: []

## 各维度最后检查时间
last_email_check_at: null
last_calendar_check_at: 2026-04-14T12:59:00+08:00
last_memory_maintenance_at: null
last_weather_check_at: null

## 检查间隔配置
check_intervals:
  email: 30
  calendar: 15
  memory_maintenance: 480
  weather: 180

## 稳定性配置
error_count_threshold: 5
heartbeat_min_interval: 300
action_timeout: 30
max_retry_per_error: 3

## 降级策略链
fallback_chain:
  - web_search
  - local_knowledge
  - ask_user