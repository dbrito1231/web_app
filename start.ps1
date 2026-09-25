#Requires -Version 5.1
<#
.SYNOPSIS
  Start the workbook Django API and Vite frontend on 127.0.0.1.
#>
$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$Backend = Join-Path $Root "backend"
$Frontend = Join-Path $Root "frontend"
$Py = Join-Path $Backend ".venv\Scripts\python.exe"
$Npm = Get-Command npm -ErrorAction SilentlyContinue

if (-not (Test-Path $Py)) {
  Write-Error "Backend venv not found at $Py. From backend\: python -m venv .venv; .\.venv\Scripts\Activate.ps1; pip install -r requirements.txt; python manage.py migrate"
}

if (-not $Npm) {
  Write-Error "npm was not found on PATH. Install Node.js, then run npm install in frontend\."
}

if (-not (Test-Path (Join-Path $Frontend "node_modules"))) {
  Write-Host "frontend\node_modules missing - running npm install..."
  Push-Location $Frontend
  try { npm install } finally { Pop-Location }
}

Write-Host "Starting Django on http://127.0.0.1:8000 ..."
Start-Process -FilePath $Py -ArgumentList @(
  "manage.py", "runserver", "127.0.0.1:8000"
) -WorkingDirectory $Backend -WindowStyle Normal

Write-Host "Starting Vite on http://127.0.0.1:5173 ..."
Start-Process -FilePath "npm" -ArgumentList @(
  "run", "dev", "--", "--host", "127.0.0.1", "--port", "5173"
) -WorkingDirectory $Frontend -WindowStyle Normal

Start-Sleep -Seconds 2
Start-Process "http://127.0.0.1:5173"

Write-Host ""
Write-Host "Workbook started."
Write-Host "  UI:  http://127.0.0.1:5173"
Write-Host "  API: http://127.0.0.1:8000"
Write-Host "Close the two new PowerShell/console windows to stop the servers."
