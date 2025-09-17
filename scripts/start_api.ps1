Param(
  [int]$Port = 8000,
  [string]$BindHost = "0.0.0.0",
  [switch]$Reload
)

$ErrorActionPreference = "Stop"

# Prefer the Python 3.11 virtualenv if present
$venvPython = Join-Path (Resolve-Path ".").Path ".venv311\Scripts\python.exe"
if (-not (Test-Path $venvPython)) {
  $venvPython = "python"
}

$argsList = "-m uvicorn api.main:app --host $BindHost --port $Port"
if ($Reload) { $argsList = "$argsList --reload" }

$outLog = "uvicorn.out.log"
$errLog = "uvicorn.err.log"
$pidFile = "uvicorn.pid"

$p = Start-Process -FilePath $venvPython -ArgumentList $argsList -RedirectStandardOutput $outLog -RedirectStandardError $errLog -PassThru
$p.Id | Set-Content $pidFile
Write-Output "Started uvicorn with PID $($p.Id) on http://localhost:$Port using '$venvPython'"
