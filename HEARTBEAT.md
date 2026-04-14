## Self-Improving Heartbeat

严格按照 `./self-improving/heartbeat-rules.md` 执行。

**完整 STR 闭环循环（每次心跳必走）：**
1. **SENSE** — 感知系统状态（上次结果、待处理任务、异常、时间上下文）
2. **THINK** — 判断优先级，决定执行策略
3. **EXECUTE** — 执行记忆整理/错误恢复/日历检查/邮件检查/定时任务
4. **EVALUATE** — 评估每个动作的成功/失败/意外
5. **LEARN** — 更新记忆、策略、经验教训

**状态机：** IDLE → PLANNING → EXECUTING → EVALUATING → LEARNED → IDLE  
**异常路径：** 任意状态遇错误 → ERROR_FATAL → RECOVERING → IDLE

> 详见 `self-improving/heartbeat-rules.md`
