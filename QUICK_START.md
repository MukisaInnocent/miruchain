# MIRUCHAIN Quick Start

## Requirements

- Windows with PowerShell
- Python 3.14 available through the `py` launcher
- Internet access on first run to install dependencies

## Run locally

From the repository root:

```powershell
.\run-local.ps1
```

The launcher creates `backend/.venv314`, installs dependencies, applies migrations to a local SQLite file at `backend/local.sqlite3`, and starts both servers. No PostgreSQL or Redis service is required for local development. The local database is ignored by Git and does not affect deployment database settings.

- Site: http://127.0.0.1:8080/index.html
- API: http://127.0.0.1:8000/api/v1/
- Django admin: http://127.0.0.1:8000/admin/

Press Ctrl+C in the launcher window to stop the servers. Use `.\run-local.ps1 -CreateSuperuser` to create a Django admin account before the servers start. The frontend admin page uses the normal application login and is separate from Django admin.

The `backend\start.ps1` and `backend\activate_and_run.bat` shortcuts invoke the same launcher. See [backend/START_HERE.md](backend/START_HERE.md) for the setup details.

## Notes

- The first run may take a few minutes while packages install.
- Email is configured to print to the backend console; Stripe credentials are optional until payment flows are tested.
- Python package versions are pinned in `backend/requirements.txt`. PostgreSQL remains the default database unless `DB_ENGINE` is explicitly overridden.
