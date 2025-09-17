Param(
  [string]$Chatwoot = $env:CHATWOOT_BASE_URL,
  [string]$AccountId = $env:CHATWOOT_ACCOUNT_ID,
  [string]$AccessToken = $env:CHATWOOT_ACCESS_TOKEN,
  [Parameter(Mandatory=$true)][int]$ConversationId,
  [Parameter(Mandatory=$true)][string]$Content,
  [ValidateSet('outgoing','incoming')][string]$MessageType = 'outgoing',
  [switch]$Private
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

if (-not $Chatwoot -or -not $AccountId -or -not $AccessToken) {
  $envPath = [System.IO.Path]::Combine($PSScriptRoot, '..', '.env')
  $envMap = Get-DotEnvValues -Path $envPath
  if (-not $Chatwoot -and $envMap.ContainsKey('CHATWOOT_BASE_URL')) { $Chatwoot = $envMap['CHATWOOT_BASE_URL'] }
  if (-not $AccountId -and $envMap.ContainsKey('CHATWOOT_ACCOUNT_ID')) { $AccountId = $envMap['CHATWOOT_ACCOUNT_ID'] }
  if (-not $AccessToken -and $envMap.ContainsKey('CHATWOOT_ACCESS_TOKEN')) { $AccessToken = $envMap['CHATWOOT_ACCESS_TOKEN'] }
}

if (-not $Chatwoot -or -not $AccountId -or -not $AccessToken) {
  throw "CHATWOOT_BASE_URL, CHATWOOT_ACCOUNT_ID e CHATWOOT_ACCESS_TOKEN são obrigatórios"
}

$base = $Chatwoot.TrimEnd('/')
$headers = @{ 'Content-Type' = 'application/json'; 'api_access_token' = $AccessToken }
$body = @{ content = $Content; message_type = $MessageType; private = [bool]$Private } | ConvertTo-Json -Depth 5
$url = "$base/api/v1/accounts/$AccountId/conversations/$ConversationId/messages"

Write-Host "POST $url" -ForegroundColor Cyan
Write-Host "Body: $body" -ForegroundColor DarkGray

try {
  $resp = Invoke-RestMethod -Method Post -Uri $url -Headers $headers -Body $body
  $json = $resp | ConvertTo-Json -Depth 8
  Write-Host "Response: $json" -ForegroundColor Green
  Write-Output $json
} catch {
  Write-Error "Account reply failed: $($_.Exception.Message)"
  if ($_.Exception.Response) { $sr = New-Object IO.StreamReader($_.Exception.Response.GetResponseStream()); Write-Error ($sr.ReadToEnd()) }
  throw
}
