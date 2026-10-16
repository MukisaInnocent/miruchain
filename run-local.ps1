param(
    [switch]$CreateSuperuser
)

$ErrorActionPreference = 'Stop'
$repoRoot = $PSScriptRoot
$backendPath = Join-Path $repoRoot 'backend'
$frontendPath = Join-Path $repoRoot 'frontend'

$pythonLauncher = Get-Command py -ErrorAction SilentlyContinue
if (-not $pythonLauncher) {
    throw 'Python 3.14 and the Windows py launcher are required. Install Python 3.14, then run this script again.'
}

$pythonExe = & $pythonLauncher.Source -3.14 -c 'import sys; print(sys.executable)' 2>$null
if ($LASTEXITCODE -ne 0 -or -not $pythonExe) {
    throw 'Python 3.14 was not found by the py launcher. Install Python 3.14, then run this script again.'
}
$pythonExe = $pythonExe.Trim()

$venvPath = Join-Path $backendPath '.venv314'
$venvPython = Join-Path $venvPath 'Scripts\python.exe'
if (-not (Test-Path $venvPython)) {
    & $pythonExe -m venv $venvPath
    if ($LASTEXITCODE -ne 0) {
        throw 'Could not create the local Python environment.'
    }
}

& $venvPython -m pip install -r (Join-Path $backendPath 'requirements.txt')
if ($LASTEXITCODE -ne 0) {
    throw 'Dependency installation failed.'
}

$environmentNames = @('SECRET_KEY', 'DEBUG', 'ALLOWED_HOSTS', 'DB_ENGINE', 'DB_NAME', 'FRONTEND_URL')
$previousEnvironment = @{}
foreach ($name in $environmentNames) {
    $previousEnvironment[$name] = [Environment]::GetEnvironmentVariable($name, 'Process')
}

$frontendProcess = $null
Push-Location $backendPath
try {
    $env:SECRET_KEY = 'local-development-only-not-for-production'
    $env:DEBUG = 'True'
    $env:ALLOWED_HOSTS = 'localhost,127.0.0.1'
    $env:DB_ENGINE = 'django.db.backends.sqlite3'
    $env:DB_NAME = Join-Path $backendPath 'local.sqlite3'
    $env:FRONTEND_URL = 'http://127.0.0.1:8080'

    & $venvPython manage.py check
    if ($LASTEXITCODE -ne 0) {
        throw 'Django configuration check failed.'
    }

    & $venvPython manage.py migrate --noinput
    if ($LASTEXITCODE -ne 0) {
        throw 'Database migration failed.'
    }

    if ($CreateSuperuser) {
        & $venvPython manage.py createsuperuser
        if ($LASTEXITCODE -ne 0) {
            throw 'Superuser creation failed.'
        }
    }

    if (Get-NetTCPConnection -LocalPort 8080 -State Listen -ErrorAction SilentlyContinue) {
        throw 'Port 8080 is already in use. Stop the other server and try again.'
    }

    $frontendProcess = Start-Process -FilePath $venvPython `
        -ArgumentList @('-m', 'http.server', '8080', '--bind', '127.0.0.1') `
        -WorkingDirectory $frontendPath `
        -WindowStyle Hidden `
        -PassThru `
        -RedirectStandardOutput (Join-Path $env:TEMP 'miruchain-frontend.log') `
        -RedirectStandardError (Join-Path $env:TEMP 'miruchain-frontend-error.log')

    Write-Host 'MIRUCHAIN is starting:' -ForegroundColor Green
    Write-Host '  Site:  http://127.0.0.1:8080/index.html'
    Write-Host '  API:   http://127.0.0.1:8000/api/v1/'
    Write-Host '  Admin: http://127.0.0.1:8000/admin/'
    Start-Process 'http://127.0.0.1:8080/index.html'

    & $venvPython manage.py runserver 127.0.0.1:8000
    if ($LASTEXITCODE -ne 0) {
        throw 'The Django development server stopped with an error.'
    }
}
finally {
    if ($frontendProcess -and -not $frontendProcess.HasExited) {
        Stop-Process -Id $frontendProcess.Id -Force
    }
    foreach ($name in $environmentNames) {
        [Environment]::SetEnvironmentVariable($name, $previousEnvironment[$name], 'Process')
    }
    Pop-Location
}