# 设计规范参考

---

## 配色方案

### 电商风格（生鲜/食品类）
```
--warm-orange: #C4622D    主按钮/强调色
--orange-light: #E07B42    次强调
--cream: #FAF7F2          背景色
--ink: #1A252C             深色文字
--text-light: #6B7D84       次要文字
--white: #FFFFFF            卡片背景
```

### 企业/品牌风格
```
--navy: #1A3A5C           主色调（深蓝）
--gold: #B8860B            强调色（金色）
--light-gray: #F5F5F5       背景
--dark: #1F2937             文字
--white: #FFFFFF            卡片
```

### 餐饮/传统行业
```
--red: #8B2500             中国红主色
--gold: #D4A017            金色强调
--cream: #FFF8E7            米黄背景
--dark-brown: #3D2914        深棕文字
```

---

## 字体方案

```html
<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@300;400;600;700&family=Noto+Sans+SC:wght@300;400;500;600&display=swap" rel="stylesheet">

<style>
body { font-family: 'Noto Sans SC', sans-serif; }
.serif { font-family: 'Noto Serif SC', serif; }
</style>
```

---

## 布局规范

### 移动端优先原则
```css
/* 先写移动端 */
.hero { padding: 40px 20px; }

/* 再写平板 */
@media (min-width: 768px) {
  .hero { padding: 80px 40px; }
}

/* 最后写桌面 */
@media (min-width: 960px) {
  .hero { padding: 100px 60px; max-width: 1100px; margin: 0 auto; }
}
```

### 常用间距
```
移动端 padding: 40px 20px
平板   padding: 60px 40px
桌面   padding: 80px 60px
section 间距: 80-100px
卡片间距: 20-30px
```

---

## Hero 设计模板

```html
<section class="hero">
  <div class="hero-bg"></div>
  <div class="hero-content">
    <div class="hero-text">
      <div class="hero-badge">🏞️ 产地直供</div>
      <h1>品牌名<span class="accent">产品名</span></h1>
      <p>核心卖点一句话</p>
      <div class="hero-actions">
        <a href="#buy" class="btn-primary">立即购买 →</a>
        <a href="#products" class="btn-secondary">查看详情</a>
      </div>
    </div>
    <div class="hero-visual">
      <img src="images/hero-product.jpg" alt="产品图">
    </div>
  </div>
</section>
```

```css
.hero {
  position: relative;
  min-height: 100vh;
  background: linear-gradient(135deg, #1A252C 0%, #2E4450 100%);
  color: white;
  display: flex;
  align-items: center;
}
.hero-bg {
  position: absolute; inset: 0;
  background-size: cover; background-position: center;
  opacity: 0.4;
}
.hero-bg::after {
  content: '';
  position: absolute; inset: 0;
  background: linear-gradient(to bottom, rgba(0,0,0,0.2), rgba(0,0,0,0.7));
}
.hero-content {
  position: relative; z-index: 2;
  max-width: 1200px; margin: 0 auto; padding: 100px 24px;
  display: grid; grid-template-columns: 1fr 1fr; gap: 48px;
}
@media (max-width: 768px) {
  .hero-content { grid-template-columns: 1fr; }
}
```

---

## 产品卡片模板

```html
<div class="product-card">
  <div class="product-img">
    <img src="images/product.jpg" alt="产品名">
    <div class="product-badge">热卖</div>
  </div>
  <div class="product-info">
    <div class="product-name">产品名</div>
    <div class="product-spec">规格描述</div>
    <div class="product-bottom">
      <div class="product-price">
        <span class="yuan">¥</span>
        <span class="num">68</span>
        <span class="unit">/只</span>
      </div>
      <button class="product-btn">订购</button>
    </div>
  </div>
</div>
```

```css
.product-card {
  background: white;
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0,0,0,0.08);
  transition: transform 0.3s, box-shadow 0.3s;
}
.product-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 16px 48px rgba(0,0,0,0.14);
}
.product-img {
  aspect-ratio: 1;
  overflow: hidden;
  position: relative;
}
.product-img img {
  width: 100%; height: 100%;
  object-fit: cover;
  transition: transform 0.5s;
}
.product-card:hover .product-img img {
  transform: scale(1.05);
}
```

---

## 常见错误

1. **Hero 用纯色背景** → 必须有真实大图或高质量渐变
2. **产品卡用 emoji 图** → 必须用真实产品照片
3. **价格只写"xx元起"** → 必须有具体规格价格
4. **评价是假数据** → 必须是真实或模拟真实买家口吻
5. **按钮文字太普通** → "立即购买" > "查看更多"
