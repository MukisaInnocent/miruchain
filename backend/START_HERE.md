# Local Windows Setup

## Requirements

- Python 3.14 installed and available through the Windows `py` launcher
- PowerShell

## Start the site

From the repository root, run:

```powershell
.\run-local.ps1
```

The first run creates `backend/.venv314`, installs the Python dependencies, and creates a local SQLite database at `backend/local.sqlite3`. It does not connect to or modify PostgreSQL. The frontend and API start at:

- Site: http://127.0.0.1:8080/index.html
- API: http://127.0.0.1:8000/api/v1/
- Admin: http://127.0.0.1:8000/admin/

Press Ctrl+C in the PowerShell window to stop both servers. To create a Django admin account, run `.\run-local.ps1 -CreateSuperuser` instead.

The PostgreSQL settings remain the default for deployments; the local launcher overrides them only for its own process.
