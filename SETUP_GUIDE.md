# Quick Setup Guide for MIRUCHAIN

## Prerequisites Check

Before starting, make sure you have:
- [ ] Python 3.10+ installed
- [ ] PostgreSQL 13+ installed and running
- [ ] Redis installed and running
- [ ] Git installed

## Step-by-Step Setup

### 1. Navigate to Project
```powershell
cd "c:\Users\MUKISA INNOCENT\Music\miruchain"
```

### 2. Create Virtual Environment (if not done)
```powershell
python -m venv venv
.\venv\Scripts\activate
```

### 3. Install Dependencies
```powershell
cd backend
pip install -r requirements.txt
```

### 4. Set Up Database

**Option A: Using psql**
```powershell
# Open PostgreSQL command line
psql -U postgres

# Then run these SQL commands:
CREATE DATABASE miruchain_db;
CREATE USER miruchain_user WITH PASSWORD 'root';
ALTER ROLE miruchain_user SET client_encoding TO 'utf8';
ALTER ROLE miruchain_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE miruchain_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE miruchain_db TO miruchain_user;
\q
```

**Option B: Using pgAdmin**
1. Open pgAdmin
2. Right-click "Databases" > "Create" > "Database"
3. Name: `miruchain_db`
4. Owner: Create user `miruchain_user` first in Login/Group Roles

### 5. Create Environment File
```powershell
# Go to project root
cd ..
copy .env.example .env
notepad .env
```

**Edit these values in .env:**
```env
SECRET_KEY=your-random-secret-key-here-make-it-long-and-random
DB_PASSWORD=YourSecurePassword123  # Same as used in database creation
```

### 6. Run Database Migrations
```powershell
cd backend
python manage.py makemigrations
python manage.py migrate
```

### 7. Create Superuser
```powershell
python manage.py createsuperuser
# Follow prompts to enter email and password
```

### 8. Start Development Server
```powershell
python manage.py runserver
```

Visit: http://localhost:8000/admin to access Django admin

### 9. (Optional) Start Celery Worker
Open a new terminal:
```powershell
cd "c:\Users\MUKISA INNOCENT\Music\miruchain"
.\venv\Scripts\activate
cd backend
celery -A miruchain worker -l info
```

## Troubleshooting

### Error: "No module named 'decouple'"
```powershell
pip install python-decouple
```

### Error: PostgreSQL connection failed
- Check if PostgreSQL service is running
- Verify database name, user, and password in .env
- Check DB_HOST is 'localhost' and DB_PORT is '5432'

### Error: Redis connection failed
- Install Redis for Windows (Memurai) or use WSL
- Or use Docker: `docker run -p 6379:6379 redis`

### Error: "ModuleNotFoundError: No module named 'miruchain'"
- Make sure you're in the `backend` directory
- Make sure virtual environment is activated

## Next Development Steps

See `BUILD_STATUS.md` for detailed progress and next steps.

Quick summary:
1. Complete Users app (views, URLs, admin)
2. Build Referrals app (commission calculation)
3. Build Links app (business links management)
4. Build Transactions app (payment integration)
5. Build Admin Panel app
6. Create Frontend templates

## Useful Commands

```powershell
# Activate virtual environment
.\venv\Scripts\activate

# Create new migration after model changes
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver

# Django shell (for testing)
python manage.py shell

# Create new app
python manage.py startapp app_name
```

## Project Documentation

All documentation is in the `docs/` folder:
- `implementation_plan.md` - Full architecture
- `database_schema.md` - Database design
- `api_documentation.md` - API endpoints
- `deployment_guide.md` - Production deployment
- `referral_commission_logic.md` - Commission calculation details

## Get Help

If you encounter issues:
1. Check `BUILD_STATUS.md` for current progress
2. Review `docs/deployment_guide.md`
3. Check Django documentation: https://docs.djangoproject.com/
4. Check error messages carefully - they usually indicate the problem

---

**All your documentation is in**: `c:\Users\MUKISA INNOCENT\Music\miruchain\docs\`
