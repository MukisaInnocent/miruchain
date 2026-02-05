# MIRUCHAIN Platform Documentation

This folder contains all planning and technical documentation for the MIRUCHAIN referral-based advertising platform.

## 📚 Documentation Index

### Planning & Design
- **[implementation_plan.md](implementation_plan.md)** - Complete technical architecture and implementation roadmap
- **[database_schema.md](database_schema.md)** - PostgreSQL database schema with tables, relationships, and indexes
- **[referral_commission_logic.md](referral_commission_logic.md)** - Detailed multi-level commission calculation logic with examples
- **[ui_wireframes.md](ui_wireframes.md)** - UI/UX design specifications with mockups
- **[api_documentation.md](api_documentation.md)** - Complete REST API endpoint documentation
- **[deployment_guide.md](deployment_guide.md)** - Deployment instructions for development and production

### UI Mockups
- **homepage_mockup.png** - Homepage design
- **dashboard_mockup.png** - Member dashboard with referral tree
- **links_directory_mockup.png** - Business links directory page
- **admin_panel_mockup.png** - Admin dashboard interface

## 🏗️ Project Structure

```
miruchain/
├── docs/                    # ← You are here
│   ├── README.md
│   ├── implementation_plan.md
│   ├── database_schema.md
│   ├── referral_commission_logic.md
│   ├── ui_wireframes.md
│   ├── api_documentation.md
│   ├── deployment_guide.md
│   └── mockups/
├── backend/                 # Django backend
│   ├── miruchain/          # Main Django app
│   ├── users/              # User authentication
│   ├── referrals/          # Referral system
│   ├── links/              # Business links
│   ├── transactions/       # Payments & transactions
│   ├── admin_panel/        # Admin functionalities
│   ├── manage.py
│   └── requirements.txt
├── frontend/               # Frontend files
│   ├── css/
│   ├── js/
│   ├── images/
│   └── templates/
├── .env                    # Environment configuration
└── README.md               # Project overview
```

## 🚀 Quick Start

1. Read **[deployment_guide.md](deployment_guide.md)** for setup instructions
2. Review **[implementation_plan.md](implementation_plan.md)** for architecture overview
3. Check **[api_documentation.md](api_documentation.md)** for API endpoints
4. See **[database_schema.md](database_schema.md)** for database structure

## 💡 Key Features

- **Multi-Level Referral System**: Earn commissions up to multiple levels deep
- **Business Link Advertising**: Post and share business links for rewards
- **Admin Panel**: Complete platform management interface
- **Payment Integration**: Secure membership and withdrawal processing
- **Real-time Analytics**: Track earnings and referral performance

## 📞 Platform Details

- **Name**: MIRUCHAIN
- **Tech Stack**: Python (Django), PostgreSQL, HTML/CSS/JavaScript
- **Architecture**: REST API with JWT authentication
- **Payment**: Stripe/PayPal integration ready

---

**Last Updated**: February 2026  
**Version**: 1.0.0-dev
