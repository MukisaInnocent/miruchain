# MIRUCHAIN - UI Wireframes & Mockups

Complete visual design reference for the MIRUCHAIN referral-based advertising platform.

---

## Design System

### Color Palette

**Primary Colors:**
- Primary Blue: `#4F46E5` (Indigo-600)
- Primary Purple: `#7C3AED` (Violet-600)
- Accent Cyan: `#06B6D4` (Cyan-500)

**Neutral Colors:**
- Dark: `#1E293B` (Slate-800)
- Medium: `#64748B` (Slate-500)
- Light: `#F1F5F9` (Slate-100)
- White: `#FFFFFF`

**Status Colors:**
- Success: `#10B981` (Green-500)
- Warning: `#F59E0B` (Amber-500)
- Error: `#EF4444` (Red-500)
- Info: `#3B82F6` (Blue-500)

### Typography

**Font Family:**
- Primary: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif
- Monospace: "Fira Code", "Courier New", monospace

**Font Sizes:**
- Heading 1: 2.5rem (40px)
- Heading 2: 2rem (32px)
- Heading 3: 1.5rem (24px)
- Body: 1rem (16px)
- Small: 0.875rem (14px)

### Spacing

Based on 8px grid system:
- xs: 4px
- sm: 8px
- md: 16px
- lg: 24px
- xl: 32px
- 2xl: 48px

### Components

**Buttons:**
- Primary: Gradient background (blue to purple), white text, rounded corners
- Secondary: Outline style, primary color border
- Sizes: Small (32px), Medium (40px), Large (48px)

**Cards:**
- White background with subtle shadow
- Border radius: 12px
- Padding: 24px
- Hover effect: Slight elevation increase

**Forms:**
- Input fields: 48px height, rounded corners, border focus state
- Labels: Small text, medium weight
- Validation: Inline error messages

---

## Page Wireframes

### 1. Homepage

![Homepage Mockup](C:/Users/MUKISA INNOCENT/.gemini/antigravity/brain/bd394aea-5cc4-4917-8a2b-f09fe372f544/homepage_mockup_1769913939751.png)

#### Layout Structure

**Header (Fixed)**
- Logo (left)
- Navigation: Homepage | Pricing | Advertising | Blog
- Auth buttons: Log In | Join Now (CTA)

**Hero Section**
- Full-width gradient background (blue to purple)
- Main headline: "Earn While You Share - Join MIRUCHAIN"
- Subheadline: "Unlock passive income through our referral advertising network. Share business links and watch your earnings grow."
- CTA buttons: "Join Now" (primary) | "Learn More" (secondary)
- Hero illustration/animation (optional)

**Features Section**
- 3-column grid on desktop, stacked on mobile
- Each feature card:
  - Icon (top)
  - Title
  - Description (2-3 lines)
  
  Cards:
  1. **Multi-Level Commissions**: Earn up to 3 levels of referral rewards
  2. **Business Link Advertising**: Post your business links for rewards
  3. **Track Your Earnings**: Real-time analytics and transparent payouts

**Social Proof Section**
- "Trusted by Leading Brands" text
- Brand logos (Shopify, Microsoft, etc.)
- Testimonial carousel

**Footer**
- Links: Legal | Privacy | Terms | Contact
- Copyright notice
- Social media icons

#### Responsive Design
- Desktop: Full hero with illustration
- Tablet: Hero text centered, features 2-column
- Mobile: Single column, condensed hero

---

### 2. Registration & Login Pages

#### Registration Page

**Layout:**
- Left side (40%): Brand image/gradient with value props
- Right side (60%): Registration form

**Form Fields:**
1. Full Name (required)
2. Email (required, validated)
3. Phone Number (optional)
4. Password (required, strength indicator)
5. Confirm Password (required)
6. Referral Code (auto-filled from URL param, optional)
7. Terms & Conditions checkbox (required)

**Form Footer:**
- "Join Now" button (full width, disabled until valid)
- "Already have an account? Log In" link

**Flow:**
1. User fills form
2. Click "Join Now"
3. Redirect to payment page for membership fee
4. After payment, email verification sent
5. Redirect to dashboard after verification

#### Login Page

**Layout:**
- Centered card (max-width: 400px)
- Simple, clean design

**Form Fields:**
1. Email
2. Password
3. Remember me (checkbox)

**Form Footer:**
- "Log In" button
- "Forgot Password?" link
- "Don't have an account? Sign Up" link

**Features:**
- JWT token stored in localStorage
- Redirect to dashboard after successful login
- Error handling for invalid credentials

---

### 3. Member Dashboard

![Dashboard Mockup](C:/Users/MUKISA INNOCENT/.gemini/antigravity/brain/bd394aea-5cc4-4917-8a2b-f09fe372f544/dashboard_mockup_1769913957157.png)

#### Layout Structure

**Top Bar**
- MIRUCHAIN logo (left)
- User profile dropdown (right)
- Notifications icon

**Stats Cards Row** (4 cards, responsive grid)
1. **Total Earnings**
   - Large number display: $12,450.00
   - Icon: trending up
   - Subtitle: "+$450 this month"

2. **Wallet Balance**
   - Large number display: $4,200.50
   - Icon: wallet
   - Action button: "Withdraw"

3. **Direct Referrals**
   - Large number: 45
   - Icon: users
   - Subtitle: "Active members"

4. **Total Links**
   - Large number: 312
   - Icon: link
   - Subtitle: "Posted links"

**Main Content Area** (2-column layout)

**Left Column (70%): Referral Tree Visualization**
- Section title: "Multi-Level Referral Tree"
- Interactive network diagram showing:
  - Level 1: Direct referrals (user avatars)
  - Level 2: Second-tier referrals
  - Level 3: Third-tier referrals
- Hover shows user details and earnings contributed
- Expand/collapse nodes
- Color-coded by activity status:
  - Green: Active
  - Gray: Inactive

**Right Column (30%): Recent Transactions**
- Section title: "Recent Transactions"
- Scrollable list of transactions:
  - Transaction icon (color-coded by type)
  - Description
  - Amount (green for earnings, red for withdrawals)
  - Time ago
- "View All" link at bottom

**Earnings Breakdown Section** (below referral tree)
- Tab navigation: Referral Commissions | Link Earnings
- Chart.js line chart showing earnings over time
- Filter options: Last 7 days | Last 30 days | Last 3 months

**Business Links Section**
- Section title: "My Business Links"
- Table or grid of posted links:
  - Link title
  - Status badge (Pending/Approved/Active)
  - Click count
  - Earnings
  - Actions: Edit | Share | View Stats
- "Post New Link" button

**Referral Tools Section**
- Unique referral link display
- Copy button (with success feedback)
- Social share buttons (WhatsApp, Facebook, Twitter, Email)
- QR code generator button

#### Responsive Design
- Desktop: Full 2-column layout
- Tablet: Stats 2x2 grid, single column content
- Mobile: All stacked, simplified referral tree

---

### 4. Business Links Directory

![Links Directory Mockup](C:/Users/MUKISA INNOCENT/.gemini/antigravity/brain/bd394aea-5cc4-4917-8a2b-f09fe372f544/links_directory_mockup_1769913971826.png)

#### Layout Structure

**Header**
- Page title: "Business Link Directory"
- Search bar (prominent, centered)
- "Post Your Link" button (if logged in)

**Filter Bar**
- Category pills: All | Tech | Finance | Services | Creative | Health | More
- Sort dropdown: Most Popular | Newest | Most Clicks

**Links Grid** (3 columns on desktop, 2 on tablet, 1 on mobile)

Each link card contains:
- **Header**
  - Business name/title (bold)
  - Category badge (colored pill)
  
- **Body**
  - Description (2-3 lines, truncated)
  - Contact icons: Website | Phone | Location
  
- **Footer**
  - Click count: "Clicks: 1,234"
  - Share button (if logged in) → generates tracking link
  - Admin badge (if admin link) with earning rate

**Card Interaction:**
- Hover: Slight elevation + border highlight
- Click share: Modal with:
  - Your unique share link
  - Copy button
  - Social share buttons
  - Potential earnings display

**Pagination**
- Bottom of page
- Page numbers with prev/next
- Items per page selector

#### Logged Out Experience
- Can view all links
- "Share" button shows "Login to Share" message
- Clicking link directly navigates (no tracking)

#### Logged In Experience
- Share button generates tracking link
- Can post own business links
- Can track performance

---

### 5. Admin Panel

![Admin Panel Mockup](C:/Users/MUKISA INNOCENT/.gemini/antigravity/brain/bd394aea-5cc4-4917-8a2b-f09fe372f544/admin_panel_mockup_1769913987424.png)

#### Layout Structure

**Sidebar Navigation** (Fixed, left side)
- MIRUCHAIN logo (top)
- Navigation items:
  - Dashboard (home icon)
  - Users (users icon)
  - Links (link icon)
  - Analytics (chart icon)
  - Config (settings icon)
- Logout button (bottom)

**Main Content Area**

### Dashboard Page

**Stats Cards Row** (4 cards)
1. **Total Users**: 12,450 (+83 last month)
2. **Active Members**: 8,900 (+2% last week)
3. **Platform Revenue**: $145,200 (+12% ytd)
4. **Pending Withdrawals**: $845 (12 requests)

**Content Grid** (2 columns)

**Left: Pending Links Approval Queue**
- Table with columns:
  - ID
  - User
  - Link
  - Date
  - Status badge
  - Actions: ✓ Approve | ✗ Reject
- Inline preview on hover
- Batch actions checkbox

**Right: Recent User Activity Feed**
- Timeline style list:
  - User avatar
  - Activity description
  - Time ago
- Activity types:
  - New registrations
  - Membership payments
  - Withdrawals
  - Link posts

### Users Page

**Features:**
- Search bar (email, name, referral code)
- Filters: All | Active | Inactive | Admins
- User table:
  - Avatar | Name | Email | Joined | Status | Actions
- Actions:
  - View Details (modal with full profile + referral tree)
  - Activate/Deactivate
  - Make Admin
  - View Transactions

### Links Page

**Tabs:**
- Pending (approval queue)
- Approved
- Rejected
- All

**Link Table:**
- Title | Posted By | Category | Clicks | Status | Actions
- Actions:
  - Preview
  - Approve/Reject
  - Edit
  - Delete

### Analytics Page

**Dashboard Sections:**
1. **Revenue Chart**: Line chart showing revenue over time
2. **User Growth**: Area chart showing user registrations
3. **Top Earners**: Leaderboard table
4. **Link Performance**: Bar chart of top-performing categories
5. **Conversion Funnel**: Visitors → Registrations → Paid Members

**Export Options:**
- Download CSV
- Date range selector
- Filter by category/user type

### Config Page

**Settings Sections:**

1. **Membership Settings**
   - Membership fee (input field)
   - Membership duration (dropdown)
   - Auto-renewal toggle

2. **Commission Settings**
   - Direct commission rate (%)
   - Upline pool rate (%)
   - Upline split rate (%)

3. **Link Settings**
   - Advertising fee
   - Auto-approval toggle
   - Categories management (add/remove)

4. **Payment Settings**
   - Payment gateway selection
   - API keys (masked)
   - Minimum withdrawal amount
   - Withdrawal fee

5. **Email Settings**
   - Email templates
   - SMTP configuration

Each section has "Save Changes" button

---

## Component Library Reference

### Buttons

```html
<!-- Primary Button -->
<button class="btn btn-primary">Join Now</button>

<!-- Secondary Button -->
<button class="btn btn-secondary">Learn More</button>

<!-- Small Button -->
<button class="btn btn-sm btn-primary">Copy</button>
```

### Cards

```html
<!-- Stat Card -->
<div class="stat-card">
  <div class="stat-icon">📈</div>
  <div class="stat-value">$12,450</div>
  <div class="stat-label">Total Earnings</div>
  <div class="stat-change positive">+$450 this month</div>
</div>

<!-- Link Card -->
<div class="link-card">
  <div class="link-header">
    <h3>Business Name</h3>
    <span class="badge badge-tech">Tech</span>
  </div>
  <p class="link-description">Description...</p>
  <div class="link-footer">
    <span class="link-clicks">Clicks: 1,234</span>
    <button class="btn btn-sm btn-primary">Share</button>
  </div>
</div>
```

### Forms

```html
<!-- Text Input -->
<div class="form-group">
  <label for="email">Email Address</label>
  <input type="email" id="email" class="form-control" placeholder="you@example.com">
  <span class="form-error">Invalid email address</span>
</div>

<!-- Select -->
<div class="form-group">
  <label for="category">Category</label>
  <select id="category" class="form-control">
    <option>Select category...</option>
    <option value="tech">Technology</option>
    <option value="finance">Finance</option>
  </select>
</div>
```

### Badges

```html
<span class="badge badge-success">Approved</span>
<span class="badge badge-warning">Pending</span>
<span class="badge badge-danger">Rejected</span>
<span class="badge badge-info">Active</span>
```

---

## Interactive Elements

### Modals

**Share Link Modal:**
- Centered overlay
- Close button (X)
- Title: "Share This Link"
- Your tracking link display
- Copy button
- Social share buttons
- Potential earnings display

**User Details Modal (Admin):**
- Full-screen overlay
- Profile information
- Referral statistics
- Transaction history
- Referral tree visualization
- Action buttons (deactivate, etc.)

### Notifications/Toasts

Position: Top-right corner

Types:
- Success (green): "Link copied to clipboard!"
- Error (red): "Payment failed. Please try again."
- Warning (amber): "Your membership expires in 3 days."
- Info (blue): "New referral joined your network!"

Auto-dismiss after 5 seconds

---

## Accessibility Considerations

1. **Keyboard Navigation**: All interactive elements accessible via Tab
2. **ARIA Labels**: Proper labels for screen readers
3. **Color Contrast**: WCAG AA compliant (4.5:1 minimum)
4. **Focus States**: Visible focus indicators
5. **Alt Text**: Descriptive alt text for all images
6. **Form Validation**: Clear error messages

---

## Mobile-First Responsive Breakpoints

```css
/* Mobile First */
.container { width: 100%; padding: 16px; }

/* Tablet */
@media (min-width: 768px) {
  .container { max-width: 720px; }
}

/* Desktop */
@media (min-width: 1024px) {
  .container { max-width: 960px; }
}

/* Large Desktop */
@media (min-width: 1280px) {
  .container { max-width: 1200px; }
}
```

**Mobile Navigation:**
- Hamburger menu for small screens
- Full-width buttons
- Simplified stats (stacked)
- Bottom navigation bar for dashboard

**Tablet Adjustments:**
- 2-column grid for features
- Collapsible sidebar for admin
- Reduced font sizes

**Touch Targets:**
- Minimum 44x44px for all clickable elements
- Increased spacing on mobile
