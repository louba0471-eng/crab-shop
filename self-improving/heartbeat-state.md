# Self-Improving Heartbeat State

## 元数据
last_heartbeat_started_at: null
last_heartbeat_ended_at: null
last_heartbeat_count: 0  # 累计心跳次数，用于强制完整循环
last_state: IDLE

## 上次执行结果
last_outcome: |
  timestamp: null
  state_before: IDLE
  actions_taken: []
  errors_encountered: []
  assessment: null  # success | partial | failed
  unexpected_results: []

## 异常管理
recent_errors: []
# 格式：{timestamp, error_type, detail, retry_count, resolved}
# 最多保留5条，自动清理超过24小时的旧错误

## 待处理动作
pending_actions: []
# 格式：{timestamp, action_type, detail, status}
# status: pending | executing | done | failed

## 定时任务
next_scheduled_tasks: []
# 格式：{timestamp, trigger_at, action_type, detail}

## 各维度最后检查时间
last_email_check_at: null
last_calendar_check_at: null
last_memory_maintenance_at: null
last_weather_check_at: null

## 检查间隔配置
check_intervals:
  email: 30  # minutes
  calendar: 15  # minutes
  memory_maintenance: 480  # minutes (8 hours)
  weather: 180  # minutes (3 hours)

## 稳定性配置
error_count_threshold: 5  # 超过此数量停止自动执行
heartbeat_min_interval: 300  # seconds (5 minutes)
action_timeout: 30  # seconds per action
max_retry_per_error: 3

## 降级策略链
fallback_chain:
  - web_search  # 优先
  - local_knowledge  # 其次
  - ask_user  # 最后

## 探索模式
exploration_mode: false
exploration_tasks: []
# 遇到未知任务类型时进入探索模式：小范围试错
