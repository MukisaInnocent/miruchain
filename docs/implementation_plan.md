# MIRUCHAIN Platform - Implementation Plan

A modern referral-based advertising platform enabling members to promote business links, earn commissions through multi-level referrals, and generate income via link sharing and engagement.

## User Review Required

> [!IMPORTANT]
> **Multi-Level Referral Commission Logic**
> 
> The proposed commission structure is:
> - **Direct Referral**: 25% of membership fee goes to direct referrer
> - **Upline Distribution**: Additional 25% distributed recursively:
>   - 50% of remaining pool → referrer's referrer
>   - Continue splitting upward until pool exhausted
> 
> **Example**: If membership fee is $100:
> - Direct referrer gets: $25
> - Remaining pool: $25
>   - Level 2 referrer gets: $12.50 (50% of $25)
>   - Level 3 referrer gets: $6.25 (50% of $12.50)
>   - Level 4 referrer gets: $3.13 (50% of $6.25)
>   - And so on...
> 
> **Please confirm this distribution model is correct before implementation.**

> [!WARNING]
> **Payment Gateway Integration**
> 
> The implementation plan assumes integration with a payment gateway (e.g., Stripe, PayPal, or local payment processors). Please specify:
> 1. Which payment provider(s) to integrate
> 2. Which currencies to support
> 3. Payout method preferences (bank transfer, mobile money, etc.)

> [!IMPORTANT]
> **Security & Compliance**
> 
> This platform handles financial transactions and personal data. Consider:
> 1. KYC (Know Your Customer) requirements
> 2. Anti-money laundering (AML) compliance
> 3. Data protection regulations (GDPR, etc.)
> 4. Tax reporting requirements
> 
> **Action needed**: Confirm regulatory requirements for your target region.

---

## Proposed Changes

### Core Application Structure

#### [NEW] [Project Root Structure](file:///c:/Users/MUKISA INNOCENT/Music/miruchain)

```
miruchain/
├── backend/                 # Django project
│   ├── miruchain/          # Main Django app
│   ├── users/              # User authentication & profiles
│   ├── referrals/          # Referral tracking & commissions
│   ├── links/              # Business link management
│   ├── transactions/       # Payment & earnings tracking
│   ├── admin_panel/        # Admin functionalities
│   └── manage.py
├── frontend/               # Static frontend files
│   ├── css/
│   ├── js/
│   ├── images/
│   └── templates/          # HTML templates
├── static/                 # Collected static files
├── media/                  # User uploads
├── requirements.txt
├── .env.example
└── README.md
```

---

### Database Layer (PostgreSQL)

#### [NEW] Database Schema Design

**Core Tables:**

1. **users**
   - id (UUID, primary key)
   - email (unique, indexed)
   - password_hash
   - full_name
   - phone_number
   - is_active (boolean)
   - is_verified (boolean)
   - membership_paid (boolean)
   - membership_expiry (datetime, nullable)
   - referral_code (unique, indexed)
   - referred_by (FK → users.id, nullable)
   - wallet_balance (decimal)
   - joined_at (timestamp)
   - last_login (timestamp)

2. **referrals**
   - id (UUID, primary key)
   - referrer_id (FK → users.id)
   - referred_id (FK → users.id)
   - level (integer) - depth in referral chain
   - commission_earned (decimal)
   - created_at (timestamp)

3. **transactions**
   - id (UUID, primary key)
   - user_id (FK → users.id)
   - transaction_type (enum: membership, advertising, referral_commission, withdrawal, link_earning)
   - amount (decimal)
   - status (enum: pending, completed, failed, cancelled)
   - payment_method (string)
   - payment_reference (string, unique)
   - description (text)
   - created_at (timestamp)
   - processed_at (timestamp, nullable)

4. **business_links**
   - id (UUID, primary key)
   - user_id (FK → users.id, nullable for admin links)
   - title (string)
   - description (text)
   - url (string)
   - category (string)
   - is_admin_link (boolean)
   - earning_rate (decimal) - for admin links
   - advertising_fee_paid (decimal)
   - status (enum: pending, approved, rejected, active, inactive)
   - total_clicks (integer)
   - total_conversions (integer)
   - total_earnings (decimal)
   - created_at (timestamp)
   - approved_at (timestamp, nullable)

5. **link_shares**
   - id (UUID, primary key)
   - link_id (FK → business_links.id)
   - shared_by (FK → users.id)
   - share_code (unique, indexed)
   - clicks (integer)
   - conversions (integer)
   - earnings (decimal)
   - created_at (timestamp)

6. **link_clicks**
   - id (UUID, primary key)
   - share_id (FK → link_shares.id)
   - ip_address (string)
   - user_agent (string)
   - referrer (string, nullable)
   - converted (boolean)
   - clicked_at (timestamp)

7. **config**
   - id (integer, primary key)
   - key (string, unique)
   - value (text)
   - description (text)
   - updated_at (timestamp)

---

### Backend - Django Application

#### [NEW] [requirements.txt](file:///c:/Users/MUKISA INNOCENT/Music/miruchain/requirements.txt)

Core dependencies:
- Django 4.2+
- psycopg2-binary (PostgreSQL adapter)
- djangorestframework (REST API)
- django-cors-headers (CORS support)
- djangorestframework-simplejwt (JWT authentication)
- python-decouple (environment variables)
- Pillow (image handling)
- celery (background tasks)
- redis (caching & celery broker)
- stripe / paypal-sdk (payment processing)

#### [NEW] [backend/miruchain/settings.py](file:///c:/Users/MUKISA INNOCENT/Music/miruchain/backend/miruchain/settings.py)

Django settings with:
- PostgreSQL database configuration
- JWT authentication settings
- CORS configuration
- Static/media file handling
- Celery configuration
- REST framework settings

#### [NEW] Users App

**Models** ([backend/users/models.py](file:///c:/Users/MUKISA INNOCENT/Music/miruchain/backend/users/models.py)):
- Custom User model extending AbstractUser
- Profile information
- Referral code generation
- Wallet balance tracking

**Views** ([backend/users/views.py](file:///c:/Users/MUKISA INNOCENT/Music/miruchain/backend/users/views.py)):
- User registration with referral code validation
- Login/logout with JWT
- Profile management
- Password reset
- Email verification

**Serializers** ([backend/users/serializers.py](file:///c:/Users/MUKISA INNOCENT/Music/miruchain/backend/users/serializers.py)):
- User registration serializer
- User profile serializer
- Authentication serializers

---

#### [NEW] Referrals App

**Models** ([backend/referrals/models.py](file:///c:/Users/MUKISA INNOCENT/Music/miruchain/backend/referrals/models.py)):
- Referral relationship tracking
- Commission calculation methods

**Services** ([backend/referrals/services.py](file:///c:/Users/MUKISA INNOCENT/Music/miruchain/backend/referrals/services.py)):
- `calculate_referral_commissions(new_user, membership_amount)` - Implements multi-level commission logic
- `get_referral_chain(user)` - Returns complete upline chain
- `get_referral_tree(user, depth)` - Returns downline tree for visualization

**Views** ([backend/referrals/views.py](file:///c:/Users/MUKISA INNOCENT/Music/miruchain/backend/referrals/views.py)):
- Get user's referral statistics
- Get referral tree (for dashboard visualization)
- Get commission earnings history

---

#### [NEW] Links App

**Models** ([backend/links/models.py](file:///c:/Users/MUKISA INNOCENT/Music/miruchain/backend/links/models.py)):
- BusinessLink model
- LinkShare model
- LinkClick model with analytics

**Views** ([backend/links/views.py](file:///c:/Users/MUKISA INNOCENT/Music/miruchain/backend/links/views.py)):
- Create business link (after payment verification)
- List/search business links (public directory)
- Generate share link
- Track link clicks
- Record conversions
- Calculate earnings

---

#### [NEW] Transactions App

**Models** ([backend/transactions/models.py](file:///c:/Users/MUKISA INNOCENT/Music/miruchain/backend/transactions/models.py)):
- Transaction model with type enum
- Payment processing status

**Services** ([backend/transactions/services.py](file:///c:/Users/MUKISA INNOCENT/Music/miruchain/backend/transactions/services.py)):
- `process_membership_payment(user, amount, payment_data)` - Handles membership payment and triggers commission distribution
- `process_advertising_payment(user, amount, link_data)` - Handles ad fee payment
- `process_withdrawal(user, amount, payout_method)` - Handles user withdrawals
- Payment gateway integration wrapper

**Views** ([backend/transactions/views.py](file:///c:/Users/MUKISA INNOCENT/Music/miruchain/backend/transactions/views.py)):
- Initiate payment
- Payment webhook handler
- Transaction history
- Withdrawal request
- Wallet balance

**Tasks** ([backend/transactions/tasks.py](file:///c:/Users/MUKISA INNOCENT/Music/miruchain/backend/transactions/tasks.py)):
- Celery tasks for async payment processing
- Automated payout scheduling

---

#### [NEW] Admin Panel App

**Views** ([backend/admin_panel/views.py](file:///c:/Users/MUKISA INNOCENT/Music/miruchain/backend/admin_panel/views.py)):
- User management (list, activate/deactivate, view details)
- Business link moderation (approve/reject)
- Create admin promotional links
- Platform configuration management
- Custom permission class for admin-only views

---

### Frontend - HTML/CSS/JavaScript

#### [NEW] Base Template & Styling

**Templates:**
- [frontend/templates/base.html](file:///c:/Users/MUKISA INNOCENT/Music/miruchain/frontend/templates/base.html) - Base template with navigation
- [frontend/css/style.css](file:///c:/Users/MUKISA INNOCENT/Music/miruchain/frontend/css/style.css) - Modern, professional styling with mobile-first approach
- [frontend/js/main.js](file:///c:/Users/MUKISA INNOCENT/Music/miruchain/frontend/js/main.js) - Common utilities and API helpers

**Design System:**
- Color scheme: Professional blues/purples with trust-building elements
- Typography: Clean, modern fonts (Inter/Roboto)
- Components: Cards, buttons, forms with consistent styling
- Responsive breakpoints: Mobile, tablet, desktop

---

#### [NEW] Public Pages

**Homepage** ([frontend/templates/index.html](file:///c:/Users/MUKISA INNOCENT/Music/miruchain/frontend/templates/index.html)):
- Hero section with value proposition
- How it works (3-step process)
- Features showcase
- Success statistics
- Call-to-action

**Registration** ([frontend/templates/register.html](file:///c:/Users/MUKISA INNOCENT/Music/miruchain/frontend/templates/register.html)):
- Registration form with referral code field (pre-filled from URL)
- Email verification flow
- Terms & conditions acceptance
- Payment integration for membership fee

**Login** ([frontend/templates/login.html](file:///c:/Users/MUKISA INNOCENT/Music/miruchain/frontend/templates/login.html)):
- Email/password login
- JWT token storage
- Remember me option
- Password reset link

---

#### [NEW] Member Dashboard

**Dashboard** ([frontend/templates/dashboard.html](file:///c:/Users/MUKISA INNOCENT/Music/miruchain/frontend/templates/dashboard.html)):

Features:
- **Earnings Overview**
  - Total earnings (card)
  - Wallet balance (card)
  - Pending earnings (card)
  - Quick withdrawal button

- **Earnings Breakdown**
  - Referral commissions table
  - Link sharing earnings table
  - Charts (Chart.js) showing earnings over time

- **Referral Section**
  - Unique referral link with copy button
  - Referral statistics (total referrals, active referrals)
  - Multi-level referral tree visualization (interactive diagram)

- **Business Links Management**
  - List of user's posted links
  - Add new link button (with payment flow)
  - Performance metrics per link

- **Transaction History**
  - Filterable transaction table
  - Export functionality

**JavaScript** ([frontend/js/dashboard.js](file:///c:/Users/MUKISA INNOCENT/Music/miruchain/frontend/js/dashboard.js)):
- API calls to fetch dashboard data
- Referral tree rendering using D3.js or similar
- Charts rendering with Chart.js
- Clipboard copy for referral link

---

#### [NEW] Business Links Directory

**Directory Page** ([frontend/templates/links.html](file:///c:/Users/MUKISA INNOCENT/Music/miruchain/frontend/templates/links.html)):
- Search bar with filters (category, keywords)
- Grid/list view toggle
- Link cards showing:
  - Title, description
  - Category badge
  - Share button (generates tracking link for logged-in users)
  - Click count
- Pagination

**Share Link Generator** ([frontend/js/links.js](file:///c:/Users/MUKISA INNOCENT/Music/miruchain/frontend/js/links.js)):
- Generate personalized share link
- Social media sharing buttons
- Copy to clipboard

---

#### [NEW] Admin Panel

**Admin Dashboard** ([frontend/templates/admin/dashboard.html](file:///c:/Users/MUKISA INNOCENT/Music/miruchain/frontend/templates/admin/dashboard.html)):
- Platform statistics cards
  - Total users
  - Active memberships
  - Total revenue
  - Pending withdrawals
- Recent activity feed
- Quick actions

**User Management** ([frontend/templates/admin/users.html](file:///c:/Users/MUKISA INNOCENT/Music/miruchain/frontend/templates/admin/users.html)):
- Searchable user table
- User details modal
- Activate/deactivate actions
- Referral chain view

**Link Moderation** ([frontend/templates/admin/links.html](file:///c:/Users/MUKISA INNOCENT/Music/miruchain/frontend/templates/admin/links.html)):
- Pending links queue
- Approve/reject actions
- Link preview

**Configuration** ([frontend/templates/admin/config.html](file:///c:/Users/MUKISA INNOCENT/Music/miruchain/frontend/templates/admin/config.html)):
- Membership fee setting
- Advertising fee setting
- Commission percentages
- Payment gateway settings

**Admin Link Creator** ([frontend/templates/admin/create-link.html](file:///c:/Users/MUKISA INNOCENT/Music/miruchain/frontend/templates/admin/create-link.html)):
- Create promotional links
- Set earning rates
- Target audience settings

---

## Verification Plan

### Automated Tests

**Backend Tests:**
```bash
# Run Django tests
python manage.py test

# Specific test cases:
# - Referral commission calculation accuracy
# - Payment processing flow
# - User authentication and authorization
# - API endpoint security
# - Database integrity constraints
```

**Commission Logic Verification:**
```python
# Unit tests for referral commission distribution
def test_single_level_commission():
    # Verify 25% direct commission
    
def test_multi_level_commission():
    # Verify recursive 25% pool distribution
    # Test with 3, 5, and 10 level chains
    
def test_commission_pool_exhaustion():
    # Verify distribution stops correctly
```

**API Tests:**
```bash
# Test all API endpoints
# - Authentication endpoints
# - User CRUD operations
# - Referral tracking
# - Transaction processing
# - Admin operations
```

### Manual Verification

**User Flows:**
1. **Registration & Onboarding**
   - Register with referral code
   - Complete payment
   - Verify commission distribution
   - Confirm email verification

2. **Dashboard Functionality**
   - View earnings
   - Check referral tree accuracy
   - Verify transaction history

3. **Business Link Flow**
   - Post business link
   - Pay advertising fee
   - Share link
   - Track clicks and earnings

4. **Admin Operations**
   - User management
   - Link moderation
   - Configuration changes
   - Analytics accuracy

**Payment Testing:**
- Use sandbox/test mode for payment gateway
- Test successful payments
- Test failed payments
- Test refunds
- Test withdrawal process

**Security Testing:**
- Authentication bypass attempts
- Authorization checks
- SQL injection prevention
- XSS prevention
- CSRF protection

### Performance Testing

- Load testing with multiple concurrent users
- Database query optimization
- API response time benchmarks
- Frontend performance (Lighthouse scores)

---

## Deployment Guide Preview

**Requirements:**
- PostgreSQL 13+ database
- Redis server
- Python 3.10+
- Web server (Gunicorn + Nginx)

**Steps:**
1. Set up production database
2. Configure environment variables
3. Collect static files
4. Run database migrations
5. Set up Celery workers
6. Configure SSL certificate
7. Set up monitoring and logging

**Environment Variables:**
```
DATABASE_URL
SECRET_KEY
ALLOWED_HOSTS
PAYMENT_GATEWAY_KEY
PAYMENT_GATEWAY_SECRET
EMAIL_HOST
EMAIL_PORT
REDIS_URL
CELERY_BROKER_URL
```
