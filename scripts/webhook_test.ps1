Param(
  [string]$ApiBase = "http://127.0.0.1:8000",
  [string]$SharedSecret = $env:CHATWOOT_WEBHOOK_SHARED_SECRET,
  [string]$Event = "message_created",
  [int]$AccountId = 1,
  [int]$ConversationId = 12345,
  [int]$MessageId = 1,
  [string]$Content = "Olá do teste webhook",
  [switch]$Sign
)

$ErrorActionPreference = "Stop"

function Get-DotEnvValues([string]$Path) {
  $map = @{}
  if (Test-Path $Path) {
    Get-Content -Path $Path | ForEach-Object {
      $line = $_.Trim()
      if (-not $line -or $line.StartsWith('#')) { return }
      if ($line -match '^(?<k>[^=\s]+)=(?<v>.*)$') {
        $k = $Matches.k.Trim()
        $v = $Matches.v.Trim()
        $map[$k] = $v
      }
    }
  }
  return $map
}

if (-not $SharedSecret) {
  $envPath = [System.IO.Path]::Combine($PSScriptRoot, '..', '.env')
  $envMap = Get-DotEnvValues -Path $envPath
  if ($envMap.ContainsKey('CHATWOOT_WEBHOOK_SHARED_SECRET')) { $SharedSecret = $envMap['CHATWOOT_WEBHOOK_SHARED_SECRET'] }
}

if (-not $SharedSecret) { throw "CHATWOOT_WEBHOOK_SHARED_SECRET is required" }

$base = $ApiBase.TrimEnd('/')
# Use the alias route registered in the router as well
$url = "$base/api/v1/webhooks/webhook-test/$SharedSecret"

$bodyObj = [ordered]@{
  event = $Event
  account = @{ id = $AccountId }
  conversation = @{ id = $ConversationId }
  message = @{ id = $MessageId; message_type = 'incoming'; content = $Content }
}
$raw = ($bodyObj | ConvertTo-Json -Depth 6 -Compress)

# Compute HMAC SHA256 signature (hex-lower)
$bytes = [System.Text.Encoding]::UTF8.GetBytes($raw)
$key = [System.Text.Encoding]::UTF8.GetBytes($SharedSecret)
$hmac = [System.Security.Cryptography.HMACSHA256]::Create()
$hmac.Key = $key
$hash = $hmac.ComputeHash($bytes)
$sig = -join ($hash | ForEach-Object { $_.ToString('x2') })

$headers = @{ 'Content-Type' = 'application/json' }
if ($Sign) { $headers['X-Chatwoot-Signature'] = $sig }

Write-Host "POST $url" -ForegroundColor Cyan
Write-Host "Body: $raw" -ForegroundColor DarkGray

$resp = Invoke-RestMethod -Method Post -Uri $url -Headers $headers -Body $raw
$json = $resp | ConvertTo-Json -Depth 8
Write-Host "Response: $json" -ForegroundColor Green
Write-Output $json
