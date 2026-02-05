@echo off
echo.
echo ============================================
echo   MIRUCHAIN - Quick Server Startup
echo ============================================
echo.

REM Navigate to backend directory
cd /d "%~dp0"

REM Check if venv exists
if not exist "venv\Scripts\activate.bat" (
    echo ERROR: Virtual environment not found!
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if Django is installed
python -c "import django" 2>nul
if errorlevel 1 (
    echo.
    echo Django not found! Installing dependencies...
    pip install -r requirements.txt
)

echo.
echo ============================================
echo   Ready! Now run these commands:
echo ============================================
echo.
echo 1. python manage.py migrate
echo 2. python manage.py createsuperuser  
echo 3. python manage.py runserver
echo.
echo ============================================

cmd /k
