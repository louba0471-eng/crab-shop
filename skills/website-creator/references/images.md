# 图片获取与处理指南

## 核心原则

**永远不要在未确认图片真实性的情况下使用任何图片。** 用 AI 识图或直接查看图片内容来验证。

---

## 图片来源优先级

### 第一优先：客户提供
客户提供的图片一定是首选，因为：
- 真实产品照片
- 无版权问题
- 符合产品真实外观

处理：保持原图质量，缩小到适当尺寸（最大 1200px 宽），保留 EXIF 信息

### 第二优先：政府/新闻网站
中国政府网站（省/市/县）通常有本地特产的高清图片，可免费使用。
- **泰州市政府**：`www.taizhou.gov.cn`（搜索当地特产/产品）
- **新华网/人民网**：新闻配图，标注来源后可参考
- **地方政府官网**：有农产品/特产专栏

下载方式：复制图片 URL，用 `curl -L --max-time 15 -o 保存.jpg "URL"` 下载

### 第三优先：图库
- **Pixabay**：`pixabay.com/zh`（需注册，图片 CC0 协议）
- **Pexels**：`pexels.com/zh`（需注册）
- **Unsplash**：`unsplash.com`（免费商用）

⚠️ 这些 CDN 在某些网络环境下无法访问，需验证

### 第四优先：电商平台商品图
京东/天猫/淘宝的商品详情页图片可参考，但要注意：
- 可能有水印
- 版权归属平台或商家
- 仅供设计参考，不能直接商用

---

## 图片验证方法

```bash
# 下载后验证图片是否有效
file 图片.jpg        # 检查文件类型
python3 -c "
from PIL import Image
img = Image.open('图片.jpg')
print(f'尺寸: {img.size}, 模式: {img.mode}')
# JPEG 有效
"
```

**必须用 AI 识图验证内容**：
用 `image` 工具分析图片内容是否与产品匹配。

---

## 图片尺寸规范

| 用途 | 建议尺寸 | 最大文件大小 |
|------|---------|-------------|
| Hero背景大图 | 1920×1080 | 500KB |
| 产品卡片图 | 800×800 | 200KB |
| 礼盒展示图 | 1200×800 | 300KB |
| 用户评价头像 | 200×200 | 50KB |

处理工具：
```bash
# 批量缩小图片（Python PIL）
python3 -c "
from PIL import Image
import os

for f in os.listdir('images/'):
    if f.endswith(('.jpg','.png')):
        img = Image.open(f'images/{f}')
        img = img.resize((1200, 1200), Image.LANCZOS)
        img.save(f'images/{f}', quality=85, optimize=True)
        print(f'优化: {f}')
"
```

---

## CSS 占位方案

当实在无法获取真实图片时，用 CSS 渐变+图形代替：

```css
/* 产品卡占位 */
.product-img {
  background: linear-gradient(145deg, #f5f0e8, #e0d5c8);
  display: flex;
  align-items: center;
  justify-content: center;
}
/* 在 HTML 中加标注 */
.product-img::after {
  content: '📦 待替换产品图';
  font-size: 14px;
  color: #999;
}
```

---

## 图片命名规范

```
crab-shop/
images/
  hero-bg.jpg          # Hero 背景大图
  product-001.jpg      # 产品图（通用名）
  product-公蟹2.5两.jpg  # 含规格的产品图
  origin-场地.jpg      # 产地/环境图
  gift-box-礼盒名.jpg  # 礼盒图
  badge-热卖.png      # 角标图
```

避免：中文名、特殊字符、空格。用英文或拼音。
