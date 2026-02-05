# MIRUCHAIN - Deployment Guide

Complete guide for deploying the MIRUCHAIN platform from development to production.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Local Development Setup](#local-development-setup)
3. [Production Deployment](#production-deployment)
4. [Environment Configuration](#environment-configuration)
5. [Database Setup](#database-setup)
6. [Security Checklist](#security-checklist)
7. [Monitoring & Maintenance](#monitoring--maintenance)
8. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### System Requirements

**Minimum (Development)**:
- CPU: 2 cores
- RAM: 4GB
- Storage: 10GB

**Recommended (Production)**:
- CPU: 4+ cores
- RAM: 8GB+
- Storage: 50GB+ SSD

### Required Software

- **Python**: 3.10 or higher
- **PostgreSQL**: 13 or higher
- **Redis**: 6.0 or higher
- **Node.js**: 16+ (for frontend build tools, optional)
- **Git**: For version control

### Additional Requirements

- **SSL Certificate**: For HTTPS (Let's Encrypt recommended)
- **Domain Name**: For production deployment
- **Payment Gateway Account**: Stripe, PayPal, or local provider
- **Email Service**: SMTP server or service (SendGrid, Mailgun, etc.)

---

## Local Development Setup

### 1. Clone or Create Project Structure

```bash
# If starting fresh
mkdir miruchain
cd miruchain

# Create project structure
mkdir -p backend/miruchain backend/users backend/referrals backend/links backend/transactions backend/admin_panel
mkdir -p frontend/css frontend/js frontend/images frontend/templates
mkdir -p static media
```

### 2. Set Up Python Virtual Environment

**Windows**:
```powershell
# Create virtual environment
python -m venv venv

# Activate
.\venv\Scripts\activate
```

**Linux/Mac**:
```bash
# Create virtual environment
python3 -m venv venv

# Activate
source venv/bin/activate
```

### 3. Install Dependencies

```bash
# Create requirements.txt
cat > requirements.txt << EOF
Django==4.2.7
psycopg2-binary==2.9.9
djangorestframework==3.14.0
django-cors-headers==4.3.0
djangorestframework-simplejwt==5.3.0
python-decouple==3.8
Pillow==10.1.0
celery==5.3.4
redis==5.0.1
stripe==7.4.0
gunicorn==21.2.0
whitenoise==6.6.0
django-extensions==3.2.3
EOF

# Install
pip install -r requirements.txt
```

### 4. Install and Configure PostgreSQL

**Windows**:
```powershell
# Download installer from https://www.postgresql.org/download/windows/
# Or use Chocolatey
choco install postgresql

# Start PostgreSQL service
net start postgresql-x64-14
```

**Linux (Ubuntu/Debian)**:
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib

# Start service
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

**Create Database**:
```bash
# Switch to postgres user
sudo -u postgres psql

# In PostgreSQL shell
CREATE DATABASE miruchain_db;
CREATE USER miruchain_user WITH PASSWORD 'your_secure_password';
ALTER ROLE miruchain_user SET client_encoding TO 'utf8';
ALTER ROLE miruchain_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE miruchain_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE miruchain_db TO miruchain_user;
\q
```

### 5. Install and Start Redis

**Windows**:
```powershell
# Download from https://github.com/microsoftarchive/redis/releases
# Or use WSL and follow Linux instructions

# Using Memurai (Redis alternative for Windows)
choco install memurai
```

**Linux (Ubuntu/Debian)**:
```bash
sudo apt install redis-server

# Start service
sudo systemctl start redis
sudo systemctl enable redis

# Test
redis-cli ping  # Should return PONG
```

### 6. Environment Configuration

Create `.env` file in project root:

```bash
# Backend root
cat > .env << EOF
# Django Settings
SECRET_KEY=your-very-long-and-random-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_NAME=miruchain_db
DB_USER=miruchain_user
DB_PASSWORD=your_secure_password
DB_HOST=localhost
DB_PORT=5432

# Redis
REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/0

# Email Configuration
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Payment Gateway (Stripe)
STRIPE_PUBLIC_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_test_...

# Application
FRONTEND_URL=http://localhost:8000
MEMBERSHIP_FEE=100.00
ADVERTISING_FEE=10.00

# JWT Settings
JWT_ACCESS_TOKEN_LIFETIME=60  # minutes
JWT_REFRESH_TOKEN_LIFETIME=1440  # minutes (24 hours)
EOF
```

### 7. Initialize Django Project

```bash
cd backend

# Create main project
django-admin startproject miruchain .

# Create apps
python manage.py startapp users
python manage.py startapp referrals
python manage.py startapp links
python manage.py startapp transactions
python manage.py startapp admin_panel
```

### 8. Configure Django Settings

Edit `backend/miruchain/settings.py`:

```python
import os
from decouple import config
from datetime import timedelta

# Basic Settings
SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='').split(',')

# Installed Apps
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third-party
    'rest_framework',
    'corsheaders',
    'rest_framework_simplejwt',
    'django_extensions',
    
    # Local apps
    'users',
    'referrals',
    'links',
    'transactions',
    'admin_panel',
]

# Middleware
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='5432'),
    }
}

# Custom User Model
AUTH_USER_MODEL = 'users.User'

# REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}

# JWT Settings
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=config('JWT_ACCESS_TOKEN_LIFETIME', default=60, cast=int)),
    'REFRESH_TOKEN_LIFETIME': timedelta(minutes=config('JWT_REFRESH_TOKEN_LIFETIME', default=1440, cast=int)),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
}

# CORS Settings
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:8000",
]

# Static Files
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media Files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Celery Configuration
CELERY_BROKER_URL = config('CELERY_BROKER_URL')
CELERY_RESULT_BACKEND = config('REDIS_URL')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
```

### 9. Run Migrations

```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

### 10. Collect Static Files

```bash
python manage.py collectstatic --noinput
```

### 11. Run Development Server

**Terminal 1 - Django**:
```bash
python manage.py runserver
```

**Terminal 2 - Celery Worker**:
```bash
celery -A miruchain worker -l info
```

**Terminal 3 - Celery Beat (Scheduled Tasks)**:
```bash
celery -A miruchain beat -l info
```

Access at: `http://localhost:8000`

---

## Production Deployment

### Option 1: Traditional Server (VPS)

#### 1. Server Setup

**Update System**:
```bash
sudo apt update
sudo apt upgrade -y
```

**Install Required Packages**:
```bash
sudo apt install python3.10 python3.10-venv python3-pip postgresql postgresql-contrib nginx redis-server git -y
```

#### 2. Clone Repository

```bash
cd /var/www
sudo git clone https://github.com/yourusername/miruchain.git
sudo chown -R $USER:$USER miruchain
cd miruchain
```

#### 3. Set Up Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn
```

#### 4. Configure Environment

Create production `.env` file:

```bash
nano .env
```

Update values:
```env
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
SECRET_KEY=generate-a-new-random-key-for-production
# ... other settings
```

#### 5. Set Up Gunicorn

Create Gunicorn systemd service:

```bash
sudo nano /etc/systemd/system/miruchain.service
```

```ini
[Unit]
Description=MIRUCHAIN Gunicorn daemon
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/miruchain/backend
Environment="PATH=/var/www/miruchain/venv/bin"
ExecStart=/var/www/miruchain/venv/bin/gunicorn \
    --workers 3 \
    --bind unix:/var/www/miruchain/miruchain.sock \
    miruchain.wsgi:application

[Install]
WantedBy=multi-user.target
```

Start service:
```bash
sudo systemctl start miruchain
sudo systemctl enable miruchain
```

#### 6. Configure Nginx

```bash
sudo nano /etc/nginx/sites-available/miruchain
```

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    client_max_body_size 10M;

    location /static/ {
        alias /var/www/miruchain/backend/staticfiles/;
    }

    location /media/ {
        alias /var/www/miruchain/backend/media/;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/var/www/miruchain/miruchain.sock;
    }
}
```

Enable site:
```bash
sudo ln -s /etc/nginx/sites-available/miruchain /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
```

#### 7. Set Up SSL with Let's Encrypt

```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

#### 8. Set Up Celery Workers

Create Celery worker service:

```bash
sudo nano /etc/systemd/system/celery-worker.service
```

```ini
[Unit]
Description=MIRUCHAIN Celery Worker
After=network.target

[Service]
Type=forking
User=www-data
Group=www-data
WorkingDirectory=/var/www/miruchain/backend
Environment="PATH=/var/www/miruchain/venv/bin"
ExecStart=/var/www/miruchain/venv/bin/celery -A miruchain worker -l info

[Install]
WantedBy=multi-user.target
```

Create Celery beat service:

```bash
sudo nano /etc/systemd/system/celery-beat.service
```

```ini
[Unit]
Description=MIRUCHAIN Celery Beat
After=network.target

[Service]
Type=simple
User=www-data
Group=www-data
WorkingDirectory=/var/www/miruchain/backend
Environment="PATH=/var/www/miruchain/venv/bin"
ExecStart=/var/www/miruchain/venv/bin/celery -A miruchain beat -l info

[Install]
WantedBy=multi-user.target
```

Start services:
```bash
sudo systemctl start celery-worker celery-beat
sudo systemctl enable celery-worker celery-beat
```

---

### Option 2: Docker Deployment

#### 1. Create Dockerfile

```dockerfile
# backend/Dockerfile
FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "miruchain.wsgi:application", "--bind", "0.0.0.0:8000"]
```

#### 2. Create docker-compose.yml

```yaml
version: '3.8'

services:
  db:
    image: postgres:14
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      POSTGRES_DB: miruchain_db
      POSTGRES_USER: miruchain_user
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    ports:
      - "5432:5432"

  redis:
    image: redis:6-alpine
    ports:
      - "6379:6379"

  web:
    build: ./backend
    command: gunicorn miruchain.wsgi:application --bind 0.0.0.0:8000
    volumes:
      - ./backend:/app
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    ports:
      - "8000:8000"
    env_file:
      - .env
    depends_on:
      - db
      - redis

  celery:
    build: ./backend
    command: celery -A miruchain worker -l info
    volumes:
      - ./backend:/app
    env_file:
      - .env
    depends_on:
      - db
      - redis

  celery-beat:
    build: ./backend
    command: celery -A miruchain beat -l info
    volumes:
      - ./backend:/app
    env_file:
      - .env
    depends_on:
      - db
      - redis

  nginx:
    image: nginx:alpine
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf
      - static_volume:/static
      - media_volume:/media
    ports:
      - "80:80"
      - "443:443"
    depends_on:
      - web

volumes:
  postgres_data:
  static_volume:
  media_volume:
```

#### 3. Deploy with Docker

```bash
docker-compose up -d --build
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

---

### Option 3: Cloud Platform (Heroku)

#### 1. Install Heroku CLI

```bash
curl https://cli-assets.heroku.com/install.sh | sh
```

#### 2. Create Heroku App

```bash
heroku login
heroku create miruchain-app
```

#### 3. Add PostgreSQL and Redis

```bash
heroku addons:create heroku-postgresql:hobby-dev
heroku addons:create heroku-redis:hobby-dev
```

#### 4. Create Procfile

```
web: gunicorn miruchain.wsgi --log-file -
worker: celery -A miruchain worker -l info
beat: celery -A miruchain beat -l info
```

#### 5. Configure Settings

```bash
heroku config:set SECRET_KEY=your-secret-key
heroku config:set DEBUG=False
heroku config:set ALLOWED_HOSTS=miruchain-app.herokuapp.com
# ... other config vars
```

#### 6. Deploy

```bash
git push heroku main
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

---

## Security Checklist

### Production Settings

- [ ] Set `DEBUG = False`
- [ ] Use strong `SECRET_KEY`
- [ ] Configure `ALLOWED_HOSTS` properly
- [ ] Enable HTTPS only
- [ ] Set secure cookie flags
- [ ] Enable CSRF protection
- [ ] Configure CORS properly
- [ ] Use environment variables for secrets
- [ ] Disable directory listing

### Database Security

- [ ] Use strong database password
- [ ] Limit database access to localhost/private network
- [ ] Enable PostgreSQL SSL connections
- [ ] Regular database backups
- [ ] Implement database access logging

### Application Security

- [ ] Implement rate limiting
- [ ] Add request throttling
- [ ] Validate all user inputs
- [ ] Sanitize database queries (use ORM)
- [ ] Implement proper authentication
- [ ] Use HTTPS for all requests
- [ ] Enable security headers

### Django Security Settings

```python
# Production security settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
```

---

## Monitoring & Maintenance

### Logging Configuration

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': '/var/log/miruchain/django.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}
```

### Monitoring Tools

**Sentry** (Error tracking):
```bash
pip install sentry-sdk
```

```python
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn="your-sentry-dsn",
    integrations=[DjangoIntegration()],
)
```

### Database Backup

```bash
# Create backup script
sudo nano /usr/local/bin/backup-miruchain-db.sh
```

```bash
#!/bin/bash
BACKUP_DIR="/var/backups/miruchain"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
mkdir -p $BACKUP_DIR

pg_dump -U miruchain_user miruchain_db | gzip > $BACKUP_DIR/miruchain_$TIMESTAMP.sql.gz

# Keep only last 30 days
find $BACKUP_DIR -name "*.sql.gz" -mtime +30 -delete
```

```bash
chmod +x /usr/local/bin/backup-miruchain-db.sh

# Add to crontab (daily at 2 AM)
crontab -e
0 2 * * * /usr/local/bin/backup-miruchain-db.sh
```

---

## Troubleshooting

### Common Issues

**1. Database Connection Error**
```
Solution: Check PostgreSQL is running and credentials are correct
sudo systemctl status postgresql
```

**2. Static Files Not Loading**
```
Solution: Collect static files and check Nginx configuration
python manage.py collectstatic --noinput
sudo systemctl restart nginx
```

**3. Celery Tasks Not Executing**
```
Solution: Check Celery worker status
sudo systemctl status celery-worker
sudo journalctl -u celery-worker -f
```

**4. 502 Bad Gateway**
```
Solution: Check Gunicorn socket and service
sudo systemctl status miruchain
ls -l /var/www/miruchain/miruchain.sock
```

### Useful Commands

```bash
# View Django logs
sudo journalctl -u miruchain -f

# View Nginx logs
sudo tail -f /var/log/nginx/error.log

# Restart all services
sudo systemctl restart miruchain celery-worker celery-beat nginx

# Check database connections
sudo -u postgres psql -c "SELECT * FROM pg_stat_activity;"

# Test API endpoint
curl -X POST https://yourdomain.com/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "test"}'
```

---

## Performance Optimization

### Database Optimization

```sql
-- Create indexes
CREATE INDEX idx_users_referred_by ON users(referred_by);
CREATE INDEX idx_referrals_referrer ON referrals(referrer_id);
CREATE INDEX idx_transactions_user_type ON transactions(user_id, transaction_type);
```

### Caching

```python
# Install
pip install django-redis

# Settings
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": config('REDIS_URL'),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}
```

### CDN for Static Files

Use Cloudflare or AWS CloudFront for static file delivery.

---

## Conclusion

Your MIRUCHAIN platform is now deployed! Make sure to:

1. Monitor logs regularly
2. Set up automated backups
3. Keep dependencies updated
4. Monitor performance metrics
5. Implement security patches promptly

For support, refer to Django documentation: https://docs.djangoproject.com/
