$localSetup = Join-Path (Split-Path -Parent $PSScriptRoot) 'run-local.ps1'
& $localSetup
exit $LASTEXITCODE
