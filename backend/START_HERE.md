# 🚀 Complete These 3 Steps to Start the Server

## Step 1: Configure PostgreSQL Password

1. **Edit the `.env` file** in the `backend` folder
2. **Find this line**: `DB_PASSWORD=your_postgres_password_here`
3. **Replace** `your_postgres_password_here` with your actual PostgreSQL password
4. **Save** the file

Example:
```
DB_PASSWORD=myactualpassword123
```

## Step 2: Create the Database

You have 2 options:

### Option A: Using pgAdmin (Easy - GUI)
1. Open **pgAdmin 4**
2. Connect to your PostgreSQL server
3. Right-click on **"Databases"**
4. Select **"Create" → "Database..."**
5. Enter database name: **miruchain_db**
6. Click **"Save"**

### Option B: Using PowerShell (Command Line)
1. Find your PostgreSQL bin folder (usually `C:\Program Files\PostgreSQL\<version>\bin`)
2. Run this command (replace the path if needed):
```powershell
& "C:\Program Files\PostgreSQL\16\bin\psql.exe" -U postgres -c "CREATE DATABASE miruchain_db;"
```

## Step 3: Run the Server

After completing steps 1 and 2, run these commands in PowerShell:

```powershell
# Make sure you're in the backend folder
cd backend

# Make sure virtual environment is activated (you should see (venv) in prompt)
# If not, run: .\venv\Scripts\activate

# Run migrations (create database tables)
python manage.py makemigrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser

# Start the server
python manage.py runserver
```

## ✅ Success!

When you see this message:
```
Starting development server at http://127.0.0.1:8000/
```

Your server is running! Open your browser and go to:
- **API**: http://localhost:8000/api/v1/
- **Admin Panel**: http://localhost:8000/admin

---

## 🆘 Troubleshooting

**Can't find psql.exe?**
- Search for "psql.exe" in Windows search
- Or check: `C:\Program Files\PostgreSQL\`
- Use pgAdmin instead (Option A)

**Password authentication failed?**
- Check your `.env` file has the correct password
- Make sure DB_USER is `postgres`

**Migration errors?**
- Make sure database `miruchain_db` exists
- Check PostgreSQL is running

**Need help?**
- Check `QUICK_START.md` for detailed guide
- Review error messages carefully
