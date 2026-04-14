# 部署平台详细指南

---

## GitHub Pages（最推荐）

### 优点
- 免费
- 永久地址
- 自动 HTTPS
- 不需要本地运行服务

### 缺点
- 首次配置稍复杂
- 不支持服务端动态内容

### 步骤

#### 1. 创建 GitHub 仓库
```bash
# 方法A：GitHub CLI（推荐）
gh repo create 仓库名 --public --source=. --remote-name=origin

# 方法B：网页创建后 clone
gh repo create my-website --public
git clone https://github.com/你的用户名/my-website
# 把文件复制进去
```

#### 2. 推送代码
```bash
cd 仓库目录
git add -A
git commit -m "init website"
git push -u origin main
```

#### 3. 启用 GitHub Pages
```bash
# 启用 Pages
gh api repos/用户名/仓库名/pages -X POST \
  -f build_type=legacy \
  -f source[branch]=main \
  -f source[path]=/
```

#### 4. 确认上线（可能需要等 1-2 分钟）
```bash
# 查看 Pages 状态
gh api repos/用户名/仓库名/pages 2>/dev/null | python3 -c "
import sys,json
d=json.load(sys.stdin)
print('地址:', d.get('html_url'))
print('状态:', d.get('status'))
"

# 验证（如果返回 404 等 2 分钟再试）
curl -sI https://用户名.github.io/仓库名/ | head -3
```

#### 5. 域名子路径问题
如果仓库名不是 `用户名.github.io`，URL 会是：
`https://用户名.github.io/仓库名/`

HTML 中所有路径要用**相对路径**或**加上 `/仓库名/` 前缀**：
```html
<!-- 相对路径（推荐） -->
<img src="images/photo.jpg">

<!-- 或绝对路径 -->
<img src="/仓库名/images/photo.jpg">
```

---

## Cloudflare Tunnel（临时测试）

### 适用场景
- 需要立即分享给用户预览
- GitHub Pages 还在配置中
- 微信内测试

### 步骤
```bash
# 1. 安装（已安装跳过）
brew install cloudflare/cloudflare/cloudflared

# 2. 启动本地服务器
cd 项目目录
python3 -m http.server 5000

# 3. 新终端窗口建立隧道
cloudflared tunnel --url http://localhost:5000
```

输出类似：
```
Your quick Tunnel has been created!
Visit it at: https://xxxx-xxxx.trycloudflare.com
```

⚠️ **每次重启 Mac URL 都变**，仅用于临时测试

---

## Vercel

### 前提
- Vercel 账号（需要 GitHub 授权）
- vercel CLI 已登录

### 步骤
```bash
npm i -g vercel
cd 项目目录
vercel --yes
```
首次需要扫码登录 GitHub 授权。

---

## 本地预览（开发阶段）

```bash
cd 项目目录
python3 -m http.server 5000
# 浏览器打开 http://localhost:5000
```

---

## 部署检查清单

- [ ] 所有图片用相对路径或正确前缀
- [ ] HTML 文件名是 `index.html`
- [ ] CSS/JS 都内联在 HTML 中（减少请求）
- [ ] 用 `curl -sI https://你的地址/` 确认返回 200
- [ ] 用 `curl -sI https://你的地址/images/xxx.jpg` 确认图片返回 200
- [ ] 手机浏览器打开确认布局正常
