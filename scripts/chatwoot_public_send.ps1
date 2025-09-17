Param(
  [string]$Chatwoot = $env:CHATWOOT_BASE_URL,
  [string]$InboxId = $env:CHATWOOT_INBOX_ID,
  [string]$PublicApiToken = $env:CHATWOOT_PUBLIC_API_TOKEN,
  [Parameter(Mandatory=$true)][string]$ContactSourceId,
  [Parameter(Mandatory=$true)][string]$ConversationId,
  [Parameter(Mandatory=$true)][string]$Content
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

# Fill from .env if missing
if (-not $Chatwoot -or -not $InboxId -or -not $PublicApiToken) {
  $envPath = [System.IO.Path]::Combine($PSScriptRoot, '..', '.env')
  $envMap = Get-DotEnvValues -Path $envPath
  if (-not $Chatwoot -and $envMap.ContainsKey('CHATWOOT_BASE_URL')) { $Chatwoot = $envMap['CHATWOOT_BASE_URL'] }
  if (-not $InboxId -and $envMap.ContainsKey('CHATWOOT_INBOX_ID')) { $InboxId = $envMap['CHATWOOT_INBOX_ID'] }
  if (-not $PublicApiToken -and $envMap.ContainsKey('CHATWOOT_PUBLIC_API_TOKEN')) { $PublicApiToken = $envMap['CHATWOOT_PUBLIC_API_TOKEN'] }
}

if (-not $Chatwoot) { throw "CHATWOOT_BASE_URL is required" }
if (-not $InboxId) { throw "CHATWOOT_INBOX_ID is required" }
if (-not $PublicApiToken) { throw "CHATWOOT_PUBLIC_API_TOKEN is required" }

$base = $Chatwoot.TrimEnd('/')
$headers = @{ 'Content-Type' = 'application/json' }
$body = @{ content = $Content; message_type = 'incoming' } | ConvertTo-Json -Depth 5
$url = "$base/public/api/v1/inboxes/$InboxId/contacts/$ContactSourceId/conversations/$ConversationId/messages?api_access_token=$PublicApiToken"

Write-Host "POST $url" -ForegroundColor Cyan
Write-Host "Body: $body" -ForegroundColor DarkGray

$resp = Invoke-RestMethod -Method Post -Uri $url -Headers $headers -Body $body
$json = $resp | ConvertTo-Json -Depth 8
Write-Host "Response: $json" -ForegroundColor Green
Write-Output $json

