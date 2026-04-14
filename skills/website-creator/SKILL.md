---
name: website-creator
description: 创建专业电商网站、产品落地页、企业官网。当用户要求"做一个网站"、"创建网页"、"做个落地页"、"做个产品展示"、"做个企业官网"时触发。支持从需求分析到线上部署完整流程。
---

# Website Creator — 专业网站创建技能

## 核心原则

**图片优先原则**：任何网站项目，图片必须优先处理。永远不要用 emoji、随机占位图或无关图片。先找到真实图片，再开始写代码。

**所见即所买**：电商店页必须用真实产品图，用户看到什么图片就会期待收到什么产品。图片错误是最严重的信任损耗。

---

## 完整工作流（四步闭环）

```
SENSE  →  DEPLOY
 ↓         ↓
DESIGN   VERIFY
 ↓
BUILD
```

---

## STEP 1 — SENSE（需求感知）

### 收集信息
1. **品牌/产品名称**：什么品牌？什么产品？
2. **核心卖点**：和竞品相比差异在哪？
3. **目标用户**：谁会来买？
4. **参考网站**：有没有参考站点？发给我看看
5. **图片资源**：客户提供图片吗？有没有版权？

### 竞品调研
搜索同类产品的优秀网站，提取：
- 设计风格（颜色/排版/布局）
- 内容结构（Hero / 产品 / 规格 / 评价 / CTA）
- 用户信任元素（背书/数据/承诺）

### 交付物
完成 SENSE 后，给用户一个简短的《网站策划案》确认：
```
品牌定位：
目标用户：
设计风格：
核心页面结构：
上线时间预期：
```

---

## STEP 2 — DESIGN（设计规划）

### 页面结构决策
根据业务目标选择结构：

**电商店铺型**（卖货）：
```
Hero大图 → 产品展示 → 规格价格 → 礼盒/套餐 → 客户评价 → 售后保障 → CTA
```

**品牌官网型**（展示）：
```
Hero → 品牌故事 → 产品/服务 → 客户案例 → 关于我们 → 联系方式
```

**落地页型**（获客）：
```
Hero强转化 → 痛点共鸣 → 解决方案 → 客户证言 → 限时CTA
```

### 技术选型
- **单页静态**：`index.html` + 内联 CSS/JS，最简单
- **多页静态**：每个页面一个 HTML 文件
- **框架**：Vue/React/Next.js（仅当需求明确需要时才用）

### 图片策略
设计开始前，必须先确认图片方案：
1. 客户提供真实图片 → 使用客户图
2. 客户无图 → 从以下来源获取真实图片：
   - **政府/新闻网站**（泰州政府、新华网等）
   - **Pixabay/Pexels**（公开版权图库）
   - **产品官网**（京东/天猫商品图）
3. 无法获取真实图 → 用 CSS 渐变/几何图形设计代替占位，**明确标注"需替换真实图片"**

---

## STEP 3 — BUILD（构建开发）

### 编码规范
- **单文件优先**：所有 CSS/JS 内联在 HTML 中，减少文件依赖
- **响应式**：移动端优先（先设计手机版，再放大到桌面）
- **字体**：使用 Google Fonts 的 Noto Sans SC + Noto Serif SC（中英文）
- **颜色变量**：CSS :root 定义主色/辅助色/文字色

### 设计风格
- **电商风格**：白底 + 橙色/深蓝强调色，产品图大而突出
- **企业风格**：深蓝/金色搭配，衬线字体，信任感强
- **简约风格**：大量留白，内容精炼，视觉焦点明确

### 内容填充
每个区块必须有：
- 真实产品图（或清晰占位标注）
- 具体数据（价格/规格/重量，不要写"xxx元起"）
- 信任背书（真实评价/认证/数据）

---

## STEP 4 — DEPLOY（部署上线）

### 方案A：GitHub Pages（永久免费，推荐）
```bash
# 1. 创建仓库
gh repo create 品牌名 --public --clone

# 2. 进入项目目录，上传代码
cd 项目目录
git add -A && git commit -m "init"
git push -u origin main

# 3. 启用 GitHub Pages
gh api repos/用户名/仓库名/pages -X POST \
  -f build_type=legacy -f source[branch]=main -f source[path]=/

# 4. 确认上线
gh api repos/用户名/仓库名/pages 2>/dev/null | python3 -c \
  "import sys,json; print(json.load(sys.stdin).get('html_url',''))"
```

### 方案B：Cloudflare Tunnel（临时测试）
```bash
# 安装 cloudflared（已安装跳过）
brew install cloudflare/cloudflare/cloudflared

# 启动本地服务器
cd 项目目录
python3 -m http.server 5000

# 新终端窗口建立隧道
cloudflared tunnel --url http://localhost:5000
```
⚠️ 临时地址，每次重启 Mac 都变，仅用于测试

### 方案C：Vercel（需要账号）
```bash
npm i -g vercel
cd 项目目录
vercel --yes
```
⚠️ 需要 Vercel 账号授权

---

## STEP 5 — VERIFY（验证上线）

### 必须验证项
- [ ] 所有图片正常加载（HTTP 200）
- [ ] 页面在手机端显示正常
- [ ] 点击"立即购买"/"联系我们"按钮可正常跳转
- [ ] 无 404 错误资源
- [ ] 页面在微信/浏览器均可打开

### 快速验证命令
```bash
# 检查页面是否正常
curl -sI https://你的域名/ | head -3

# 检查图片是否正常
curl -sI https://你的域名/images/产品图.jpg | head -3
```

---

## 常见问题处理

### 微信内置浏览器打不开
- 临时 tunnel 在微信会被拦截，换 GitHub Pages
- 如果 GitHub Pages 也被拦截，考虑备案或换域名

### 图片无法下载（网络受限）
- Wikimedia Commons/Pixabay 可能无法直接下载
- 解决方案：找政府/新闻网站图片（通常可访问）
- 或用 AI 图片生成工具生成真实感产品图
- 或用 CSS 图形+产品描述代替，等客户提供真实图

### 页面空白/404
- 确认文件路径：HTML 里图片引用是否用相对路径？
- GitHub Pages 的子路径：如果是 `username.github.io/repo/`，所有资源路径要加 `/repo/` 前缀

---

## 参考资源

详细指南见 references/ 目录：
- `references/deployment.md` — 各平台部署详细步骤
- `references/design.md` — 设计规范（颜色/字体/布局模板）
- `references/images.md` — 图片获取与处理指南

