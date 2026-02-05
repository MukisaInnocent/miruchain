# 🚀 MIRUCHAIN - QUICK START GUIDE

## Get Your Platform Running in 15 Minutes!

This guide will help you set up and run MIRUCHAIN locally for testing before deployment.

---

## 📋 Prerequisites

Before you begin, make sure you have:

- [ ] Python 3.8 or higher
- [ ] PostgreSQL 12 or higher
- [ ] Git (for version control)
- [ ] A code editor (VS Code recommended)

---

## ⚡ Quick Setup (Step-by-Step)

### Step 1: Verify Project Structure

Your project should look like this:

```
miruchain/
├── backend/           ← Django backend
├── frontend/          ← HTML/CSS/JS frontend
├── docs/              ← Documentation
└── *.md files         ← Project documentation
```

### Step 2: Set Up PostgreSQL Database

**Option A: Using pgAdmin (GUI)**
1. Open pgAdmin
2. Right-click on "Databases"
3. Select "Create" → "Database"
4. Name: `miruchain_db`
5. Owner: your postgres user
6. Click "Save"

**Option B: Using Command Line**
```powershell
# Open PowerShell as Administrator
psql -U postgres

# In PostgreSQL prompt:
CREATE DATABASE miruchain_db;
\q
```

### Step 3: Configure Environment Variables

1. Navigate to your project root:
   ```powershell
   cd "c:\Users\MUKISA INNOCENT\Music\miruchain"
   ```

2. Copy the example environment file:
   ```powershell
   copy .env.example .env
   ```

3. Edit `.env` with your settings:
   ```env
   # Django Settings
   DEBUG=True
   SECRET_KEY=your-secret-key-here-change-this-in-production
   ALLOWED_HOSTS=localhost,127.0.0.1
   
   # Database (Update these!)
   DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/miruchain_db
   
   # Membership Fee
   MEMBERSHIP_FEE=30.00
   
   # Stripe (Get from https://stripe.com)
   STRIPE_PUBLIC_KEY=pk_test_YOUR_KEY
   STRIPE_SECRET_KEY=sk_test_YOUR_KEY
   STRIPE_WEBHOOK_SECRET=whsec_YOUR_SECRET
   
   # Email (Optional for testing)
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_USE_TLS=True
   EMAIL_HOST_USER=your-email@gmail.com
   EMAIL_HOST_PASSWORD=your-app-password
   DEFAULT_FROM_EMAIL=noreply@miruchain.com
   ```

### Step 4: Set Up Backend

1. Open PowerShell and navigate to backend:
   ```powershell
   cd backend
   ```

2. Create virtual environment:
   ```powershell
   python -m venv venv
   ```

3. Activate virtual environment:
   ```powershell
   .\venv\Scripts\Activate
   ```

4. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```

   **If this fails**, install individually:
   ```powershell
   pip install django djangorestframework django-cors-headers
   pip install djangorestframework-simplejwt psycopg2-binary
   pip install python-dotenv stripe pillow celery redis
   ```

5. Run migrations:
   ```powershell
   python manage.py makemigrations
   python manage.py migrate
   ```

6. Create admin user:
   ```powershell
   python manage.py createsuperuser
   ```
   
   Enter:
   - Email: admin@miruchain.com
   - Password: (choose a strong password)
   - Full name: Admin User

7. Start the backend server:
   ```powershell
   python manage.py runserver
   ```

   ✅ **Backend running at:** http://localhost:8000

### Step 5: Test Backend

1. Keep the backend running in one PowerShell window

2. Open your browser and visit:
   - Admin panel: http://localhost:8000/admin
   - Login with admin credentials
   - Verify you can access the admin interface

3. Test API endpoints:
   - API root: http://localhost:8000/api/v1/
   - Should show "MIRUCHAIN API" message

### Step 6: Set Up Frontend

1. Open a NEW PowerShell window

2. Navigate to frontend:
   ```powershell
   cd "c:\Users\MUKISA INNOCENT\Music\miruchain\frontend"
   ```

3. **Option A: Using Python HTTP Server**
   ```powershell
   python -m http.server 8080
   ```

4. **Option B: Using VS Code Live Server**
   - Open `frontend` folder in VS Code
   - Right-click on `index.html`
   - Select "Open with Live Server"

   ✅ **Frontend running at:** http://localhost:8080

### Step 7: Test the Complete Application

1. **Homepage**: http://localhost:8080/index.html
   - Should see beautiful gradient hero section
   - "Join MIRUCHAIN" buttons
   - Features section

2. **Registration**: http://localhost:8080/register.html
   - Try registering a new user
   - Test referral code field

3. **Login**: http://localhost:8080/login.html
   - Login with registered user
   - Should redirect to dashboard

4. **Dashboard**: http://localhost:8080/dashboard.html
   - View stats
   - Copy referral link
   - Check earnings

5. **Business Links**: http://localhost:8080/links.html
   - Browse links (may be empty initially)
   - Try posting a new link

6. **Admin Panel**: http://localhost:8080/admin.html
   - Login as admin user
   - View platform stats
   - Test moderation features

---

## 🎯 Creating Test Data

To fully test the platform, create some test data:

### 1. Create Test Users via Django Admin

1. Go to http://localhost:8000/admin
2. Click "Users"
3. Click "Add User"
4. Create 3-5 test users with different referral relationships

### 2. Or Use Django Shell

```powershell
cd backend
python manage.py shell
```

```python
from users.models import User
from decimal import Decimal

# Create first user (no referrer)
user1 = User.objects.create_user(
    email='user1@test.com',
    password='password123',
    full_name='Test User 1',
    membership_paid=True
)

# Create second user (referred by user1)
user2 = User.objects.create_user(
    email='user2@test.com',
    password='password123',
    full_name='Test User 2',
    referrer=user1,
    membership_paid=True
)

# Add some wallet balance for testing
user1.wallet_balance = Decimal('100.00')
user1.save()

print("Test users created!")
```

### 3. Create Test Business Links

Via admin panel or shell:

```python
from links.models import BusinessLink
from users.models import User

admin = User.objects.get(email='admin@miruchain.com')

BusinessLink.objects.create(
    user=admin,
    title='Amazing Tech Product',
    url='https://example.com/product',
    description='A revolutionary tech product',
    category='Technology',
    status='approved'
)

print("Test link created!")
```

---

## 🔧 Troubleshooting

### Backend won't start?

**Error: "No module named 'django'"**
```powershell
# Make sure venv is activated
.\venv\Scripts\Activate
pip install django
```

**Error: "FATAL: database does not exist"**
```powershell
# Create the database
psql -U postgres
CREATE DATABASE miruchain_db;
\q
```

**Error: "Secret key not set"**
- Edit `.env` file
- Set SECRET_KEY to any random string

### Frontend not connecting to backend?

**CORS Error in browser console?**
- Backend `settings.py` should have CORS configured
- Check `CORS_ALLOWED_ORIGINS` includes `http://localhost:8080`

**API calls failing?**
- Verify backend is running on port 8000
- Check browser console for errors
- Verify `API_BASE_URL` in `frontend/js/api.js`

### Can't login?

**"Invalid credentials" error?**
- Verify user exists in Django admin
- Check if password is correct
- Create new user via admin panel

**JWT token errors?**
- Clear browser localStorage
- Try logging in again

---

## 📝 Common Tasks

### Reset Database
```powershell
cd backend
python manage.py flush
python manage.py migrate
python manage.py createsuperuser
```

### Check Logs
```powershell
# Backend logs show in PowerShell where server is running
# Look for errors in red text
```

### Update Backend Code
```powershell
cd backend
python manage.py makemigrations
python manage.py migrate
```

### Restart Backend
```powershell
# Press Ctrl+C to stop
python manage.py runserver
```

---

## ✅ Success Checklist

Mark each when working:

- [ ] PostgreSQL database created
- [ ] Backend virtual environment activated
- [ ] Dependencies installed
- [ ] Migrations run successfully
- [ ] Superuser created
- [ ] Backend server running (port 8000)
- [ ] Admin panel accessible
- [ ] Frontend server running (port 8080)
- [ ] Homepage loads correctly
- [ ] Can register new user
- [ ] Can login
- [ ] Dashboard shows stats
- [ ] Can browse links
- [ ] Admin panel works

---

## 🚀 Next Steps

Once everything is working locally:

1. **Test All Features**
   - User registration flow
   - Referral system
   - Link posting and sharing
   - Withdrawal requests
   - Admin moderation

2. **Add Real Stripe Keys**
   - Get from https://stripe.com
   - Update `.env` file
   - Test payment flow

3. **Configure Email**
   - Set up Gmail app password or SendGrid
   - Update email settings in `.env`
   - Test password reset emails

4. **Prepare for Deployment**
   - Review `docs/deployment_guide.md`
   - Choose hosting provider
   - Set up production database
   - Deploy!

---

## 💡 Pro Tips

1. **Keep Two PowerShell Windows Open**
   - One for backend
   - One for frontend

2. **Use Django Admin Extensively**
   - Great for testing
   - Create test data easily
   - View database directly

3. **Check Browser Console**
   - F12 in Chrome/Edge
   - See API call errors
   - Debug JavaScript issues

4. **Use Postman or Thunder Client**
   - Test API endpoints directly
   - Verify backend responses
   - Debug issues faster

5. **Read the Logs**
   - Backend errors show in PowerShell
   - Frontend errors in browser console
   - Both are helpful for debugging

---

## 📞 Need Help?

- Check `PROJECT_COMPLETE.md` for full documentation
- Review `docs/` folder for detailed guides
- Backend API docs: `docs/api_documentation.md`
- Database schema: `docs/database_schema.md`

---

**Your MIRUCHAIN platform is ready to run! Let's get it started! 🚀**
