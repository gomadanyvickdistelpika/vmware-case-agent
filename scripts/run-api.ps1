$projectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $projectRoot
& ".\.venv\Scripts\python.exe" -m uvicorn dany_super_agent.api:app --host 127.0.0.1 --port 8000

