# System 领域经验

> 文件管理、系统操作、Workspace 管理

## Workspace 文件操作

### 读/写/编辑
- `read`：文本文件，支持 offset/limit 分页
- `write`：覆盖写入，自动创建父目录
- `edit`：精确替换，用于小幅修改

### 目录操作
- 使用 `exec` 执行 shell 命令（ls/cd 等）
- 注意路径是 workspace 根目录：`/Users/yu/.openclaw/workspace`

## Git 操作

### 提交流程
```bash
git add -A
git commit -m "描述"
git push（如果已配置远程）
```

---

## 经验教训

1. **workspace 就是全局根目录**，所有相对路径都基于此
2. **重要文件修改后要 commit**，防止丢失
3. **trash > rm**，删除前考虑能否恢复
