# OpenClaw 服务配置

## 开机自启服务

两个 LaunchAgent 都是 KeepAlive=true + RunAtLoad=true，每次开机自动启动，无需手动干预：

1. **OpenClaw Gateway**：`~/Library/LaunchAgents/ai.openclaw.gateway.plist`（端口 18789）
2. **OpenClaw Control Center**：`~/Library/LaunchAgents/ai.openclaw.control-center.plist`（端口 4310）

## 已记录

- Control Center 安装路径：`~/openclaw-control-center`
- 启动命令：`npm run dev:ui`
- 两个服务各自独立运行，gateway 不依赖 control-center
