# Self-Improving Heartbeat State

## 元数据
last_heartbeat_started_at: 2026-04-14T11:20:00+08:00
last_heartbeat_ended_at: 2026-04-14T11:20:30+08:00
last_heartbeat_count: 4
last_state: IDLE

## 上次执行结果
last_outcome: |
  timestamp: 2026-04-14T11:20:00+08:00
  state_before: LEARNED
  actions_taken:
    - SENSE: 检查状态（heartbeat_count=3, 无异常，无pending）
    - THINK: 经验库无待处理，常规检查未到期，触发快速路径
    - EXECUTE: 仅更新心跳时间，未执行完整5步（快速路径）
  errors_encountered: []
  assessment: success
  note: 快速路径执行，状态正常

## 异常管理
recent_errors: []

## 待处理动作
pending_actions: []

## 待用户确认（置信度不足）
pending_review: []

## 定时任务
next_scheduled_tasks: []

## 探索模式
exploration_mode: false
exploration_tasks: []

## 各维度最后检查时间
last_email_check_at: null
last_calendar_check_at: null
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