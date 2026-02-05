# MIRUCHAIN - Background Images Guide

## Available Background Images

All background images are located in `frontend/images/` directory:

### 🎨 Generated Professional Backgrounds

1. **dashboard_modern_bg.png**
   - Dark navy/purple gradient with hexagonal tech patterns
   - Use for: Dashboard page
   - Theme: Professional, financial, data-driven

2. **business_links_bg.png**
   - Bright white/blue gradient with network connection lines
   - Use for: Business Links marketplace page
   - Theme: Clean, bright, content-focused

3. **admin_panel_bg.png**
   - Light gray with subtle grid pattern and geometric shapes
   - Use for: Admin panel page
   - Theme: Minimal, organized, data-driven

4. **auth_pages_bg.png**
   - Soft purple/blue gradient with flowing waves and particles
   - Use for: Login & Register pages
   - Theme: Secure, welcoming, modern

5. **profile_settings_bg.png**
   - Soft blue/white gradient with circular patterns
   - Use for: Profile settings page
   - Theme: Personal, clean, professional

6. **hero_background.png** *(existing)*
   - Use for: Homepage hero section

7. **dashboard_bg.png** *(existing)*
   - Use for: Alternative dashboard background

## How to Apply Backgrounds

### Method 1: Direct Background Image
```css
body {
    background: url('images/background_name.png') center/cover no-repeat fixed;
}
```

### Method 2: Background with Overlay (Recommended)
```css
body::before {
    content: '';
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: url('images/background_name.png') center/cover no-repeat;
    opacity: 0.4; /* Adjust opacity */
    z-index: -1;
}
```

### Method 3: Section-Specific Background
```css
.section-name {
    position: relative;
    background: url('images/background_name.png') center/cover no-repeat;
}

.section-name::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.5); /* Dark overlay */
    z-index: 0;
}
```

## Page-Specific Recommendations

| Page | Background Image | Opacity |
|------|-----------------|---------|
| Homepage | hero_background.png | 0.15 |
| Dashboard | dashboard_modern_bg.png | 0.4 |
| Login/Register | auth_pages_bg.png | 0.3 |
| Business Links | business_links_bg.png | 0.2 |
| Admin Panel | admin_panel_bg.png | 0.15 |
| Profile | profile_settings_bg.png | 0.25 |
| Transactions | dashboard_modern_bg.png | 0.35 |
| Referrals | business_links_bg.png | 0.3 |

## Best Practices

1. **Opacity Control**: Use 0.15-0.4 opacity for readability
2. **Fixed Position**: Use `fixed` positioning for scroll effects
3. **Overlay Technique**: Add dark/light overlays for better text contrast
4. **Performance**: Optimize images (already done at 1920x1080)
5. **Responsive**: Images scale automatically with `cover`

## Dark/Light Theme Adaptation

```css
/* Light Theme */
[data-theme="light"] body::before {
    opacity: 0.2;
}

/* Dark Theme */
[data-theme="dark"] body::before {
    opacity: 0.4;
    filter: brightness(0.8);
}
```
