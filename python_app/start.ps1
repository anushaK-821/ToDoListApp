$ErrorActionPreference = "Stop"
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptDir

$venvPython = Join-Path $scriptDir ".venv\Scripts\python.exe"

if (-not (Test-Path $venvPython)) {
    Write-Host "Creating virtual environment..."
    python -m venv .venv
}

if (-not (Test-Path $venvPython)) {
    throw "Python virtual environment was not created."
}

Write-Host "Installing dependencies..."
& $venvPython -m pip install -r requirements.txt

if (-not (Test-Path ".env") -and (Test-Path ".env.example")) {
    Write-Host "Creating .env from .env.example..."
    Copy-Item ".env.example" ".env"
}

Write-Host "Seeding default user if needed..."
& $venvPython seed_user.py

Write-Host "Starting Flask app on http://127.0.0.1:5000 ..."
& $venvPython app.py
