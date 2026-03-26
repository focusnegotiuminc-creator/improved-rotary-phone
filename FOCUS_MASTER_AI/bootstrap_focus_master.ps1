Write-Host "Initializing FOCUS MASTER AI..."

if (-not (Test-Path ".venv")) {
    python -m venv .venv
}

& ".\.venv\Scripts\Activate.ps1"
pip install -r requirements.txt

if (-not (Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
    Write-Host "Created .env from .env.example. Add your real keys before live integrations."
}

Write-Host "FOCUS MASTER AI ready. Run: python main.py"

