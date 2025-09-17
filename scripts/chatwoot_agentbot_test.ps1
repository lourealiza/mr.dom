Param(
  [string]$ApiBase = "http://127.0.0.1:8000",
  [string]$SharedSecret,
  [int]$AccountId = 1,
  [int]$ConversationId = 99,
  [int]$MessageId = 700,
  [string]$Content = "Oi bot (teste agentbot)"
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
  if ($envMap.ContainsKey('HMAC_SECRET')) { $SharedSecret = $envMap['HMAC_SECRET'] }
  elseif ($envMap.ContainsKey('CHATWOOT_WEBHOOK_SECRET')) { $SharedSecret = $envMap['CHATWOOT_WEBHOOK_SECRET'] }
}

if (-not $SharedSecret) { throw "HMAC secret (HMAC_SECRET/CHATWOOT_WEBHOOK_SECRET) is required" }

$base = $ApiBase.TrimEnd('/')
$url = "$base/api/v1/webhooks/agentbot"

$bodyObj = [ordered]@{
  event = 'message_created'
  account = @{ id = $AccountId }
  conversation = @{ id = $ConversationId }
  message = @{ id = $MessageId; message_type = 'incoming'; content = $Content }
}
$raw = ($bodyObj | ConvertTo-Json -Depth 6 -Compress)

# HMAC SHA256 signature over raw body
$bytes = [System.Text.Encoding]::UTF8.GetBytes($raw)
$key = [System.Text.Encoding]::UTF8.GetBytes($SharedSecret)
$hmac = [System.Security.Cryptography.HMACSHA256]::Create()
$hmac.Key = $key
$hash = $hmac.ComputeHash($bytes)
$sig = -join ($hash | ForEach-Object { $_.ToString('x2') })

$headers = @{ 'Content-Type' = 'application/json'; 'X-Chatwoot-Signature' = $sig }

Write-Host "POST $url" -ForegroundColor Cyan
Write-Host "Body: $raw" -ForegroundColor DarkGray

$resp = Invoke-RestMethod -Method Post -Uri $url -Headers $headers -Body $raw
$json = $resp | ConvertTo-Json -Depth 8
Write-Host "Response: $json" -ForegroundColor Green
Write-Output $json

