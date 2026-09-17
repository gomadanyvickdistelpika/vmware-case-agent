$ErrorActionPreference = "Stop"
$projectRoot = Split-Path -Parent $PSScriptRoot
$venv = Join-Path $projectRoot ".venv"
if (-not (Test-Path $venv)) {
    if (Get-Command py -ErrorAction SilentlyContinue) {
        py -3.11 -m venv $venv
    } elseif (Get-Command python -ErrorAction SilentlyContinue) {
        python -m venv $venv
    } else {
        throw "Python 3.11+ was not found. Install it from python.org and reopen PowerShell."
    }
}
& (Join-Path $venv "Scripts\python.exe") -m pip install -e "$projectRoot[dev]"
Write-Host "Start these in two PowerShell windows:"
Write-Host "  .\.venv\Scripts\python -m uvicorn dany_super_agent.api:app --reload"
Write-Host "  .\.venv\Scripts\python -m streamlit run dany_super_agent\frontend.py"
