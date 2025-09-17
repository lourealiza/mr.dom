Param(
  [int]$Port = 8010,
  [string]$BindHost = "0.0.0.0",
  [switch]$Reload
)

$ErrorActionPreference = "Stop"

# Prefer Python from .venv311 if available
$venvPython = Join-Path (Resolve-Path ".").Path ".venv311\Scripts\python.exe"
if (-not (Test-Path $venvPython)) { $venvPython = "python" }

$argsList = "-m uvicorn app:app --host $BindHost --port $Port"
if ($Reload) { $argsList = "$argsList --reload" }

$outLog = "uvicorn.out.log"
$errLog = "uvicorn.err.log"
$pidFile = "uvicorn.pid"

$p = Start-Process -FilePath $venvPython -ArgumentList $argsList -RedirectStandardOutput $outLog -RedirectStandardError $errLog -PassThru
$p.Id | Set-Content $pidFile
Write-Output "Started RAG API with PID $($p.Id) on http://localhost:$Port using '$venvPython'"

