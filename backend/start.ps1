# MIRUCHAIN Quick Start Script
# Run these commands in order

Write-Host "=== MIRUCHAIN Setup ===" -ForegroundColor Green
Write-Host ""

# Step 1: Check if virtual environment is activated
if ($env:VIRTUAL_ENV) {
    Write-Host "✓ Virtual environment activated" -ForegroundColor Green
} else {
    Write-Host "✗ Virtual environment not activated!" -ForegroundColor Red
    Write-Host "Run: .\venv\Scripts\activate" -ForegroundColor Yellow
    exit
}

# Step 2: Check PostgreSQL password
Write-Host ""
Write-Host "Step 1: Configure PostgreSQL" -ForegroundColor Cyan
Write-Host"Please edit backend\.env file and set your PostgreSQL password:" -ForegroundColor Yellow
Write-Host "  DB_PASSWORD=your_actual_postgres_password" -ForegroundColor White
Read-Host "Press Enter when done"

# Step 3: Create database
Write-Host ""
Write-Host "Step 2: Create Database" -ForegroundColor Cyan
Write-Host "Open pgAdmin or run this in PostgreSQL:" -ForegroundColor Yellow
Write-Host "  CREATE DATABASE miruchain_db;" -ForegroundColor White
Read-Host "Press Enter when database is created"

# Step 4: Run migrations
Write-Host ""
Write-Host "Step 3: Running Migrations..." -ForegroundColor Cyan
python manage.py makemigrations
python manage.py migrate

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Migrations completed!" -ForegroundColor Green
} else {
    Write-Host "✗ Migration failed!" -ForegroundColor Red
    exit
}

# Step 5: Create superuser
Write-Host ""
Write-Host "Step 4: Create Admin User" -ForegroundColor Cyan
python manage.py createsuperuser

# Step 6: Start server
Write-Host ""
Write-Host "=== Starting Server ===" -ForegroundColor Green
Write-Host "Server will start at: http://localhost:8000" -ForegroundColor Cyan
Write-Host "Admin panel: http://localhost:8000/admin" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

python manage.py runserver
