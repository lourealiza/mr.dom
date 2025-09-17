Param(
  [string]$Identifier = "lead-123",
  [string]$Name = "Alice Teste",
  [string]$Email = "alice@acme.com",
  [string]$Message = "Olá, chegou aí (API-DEV)",
  [string]$Chatwoot = $env:CHATWOOT_BASE_URL,
  [string]$InboxId = $env:CHATWOOT_INBOX_ID,
  [string]$PublicApiToken = $env:CHATWOOT_PUBLIC_API_TOKEN
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
if (-not $PublicApiToken) { throw "CHATWOOT_PUBLIC_API_TOKEN (public api token) is required" }

$base = $Chatwoot.TrimEnd('/')
$headersJson = @{ 'Content-Type' = 'application/json' }

Write-Host "Using Chatwoot: $base" -ForegroundColor Cyan
Write-Host "Inbox: $InboxId" -ForegroundColor Cyan

try {
  # 1) Create contact
  $contactBody = @{ identifier = $Identifier; name = $Name; email = $Email } | ConvertTo-Json -Depth 5
  $url1 = "$base/public/api/v1/inboxes/$InboxId/contacts?api_access_token=$PublicApiToken"
  $resp1 = Invoke-RestMethod -Method Post -Uri $url1 -Headers $headersJson -Body $contactBody
  $CONTACT_ID = $null
  $CONTACT_SOURCE_ID = $null
  if ($resp1.PSObject.Properties.Name -contains 'id') { $CONTACT_ID = $resp1.id }
  if ($resp1.PSObject.Properties.Name -contains 'source_id') { $CONTACT_SOURCE_ID = $resp1.source_id }
  if (-not $CONTACT_ID -and $resp1.PSObject.Properties.Name -contains 'contact') {
    if ($resp1.contact.id) { $CONTACT_ID = $resp1.contact.id }
    if ($resp1.contact.source_id) { $CONTACT_SOURCE_ID = $resp1.contact.source_id }
  }
  if (-not $CONTACT_SOURCE_ID) { $CONTACT_SOURCE_ID = $CONTACT_ID }
  if (-not $CONTACT_SOURCE_ID) { throw "Failed to obtain CONTACT identifiers from response: $($resp1 | ConvertTo-Json -Depth 8)" }
  Write-Host ("CONTACT_ID={0}" -f $CONTACT_ID) -ForegroundColor Green
  Write-Host ("CONTACT_SOURCE_ID={0}" -f $CONTACT_SOURCE_ID) -ForegroundColor Green

  # 2) Create conversation
  # Chatwoot Public API expects contact_source_id on the URL path
  $url2 = "$base/public/api/v1/inboxes/$InboxId/contacts/$CONTACT_SOURCE_ID/conversations?api_access_token=$PublicApiToken"
  $resp2 = Invoke-RestMethod -Method Post -Uri $url2 -Headers $headersJson -Body '{}'
  $CVID = $null
  if ($resp2.PSObject.Properties.Name -contains 'id') { $CVID = $resp2.id }
  elseif ($resp2.PSObject.Properties.Name -contains 'conversation' -and $resp2.conversation.id) { $CVID = $resp2.conversation.id }
  if (-not $CVID) { throw "Failed to obtain conversation id from response: $($resp2 | ConvertTo-Json -Depth 8)" }
  Write-Host ("CVID={0}" -f $CVID) -ForegroundColor Green

  # 3) Send incoming message
  $msgBody = @{ content = $Message; message_type = 'incoming' } | ConvertTo-Json -Depth 5
  $url3 = "$base/public/api/v1/inboxes/$InboxId/contacts/$CONTACT_SOURCE_ID/conversations/$CVID/messages?api_access_token=$PublicApiToken"
  $resp3 = Invoke-RestMethod -Method Post -Uri $url3 -Headers $headersJson -Body $msgBody
  $MID = $null
  if ($resp3.PSObject.Properties.Name -contains 'id') { $MID = $resp3.id }
  elseif ($resp3.PSObject.Properties.Name -contains 'message' -and $resp3.message.id) { $MID = $resp3.message.id }
  if (-not $MID) { throw "Failed to obtain message id from response: $($resp3 | ConvertTo-Json -Depth 8)" }
  Write-Host ("MESSAGE_ID={0}" -f $MID) -ForegroundColor Green

  # Summary output for scripting
  Write-Output ("CONTACT_ID={0}" -f $CONTACT_ID)
  Write-Output ("CVID={0}" -f $CVID)
  Write-Output ("MESSAGE_ID={0}" -f $MID)

} catch {
  Write-Error "Chatwoot demo failed: $($_.Exception.Message)"
  if ($_.Exception.Response -and ($_.Exception.Response -is [System.Net.HttpWebResponse])) {
    $resp = $_.Exception.Response
    Write-Error ("HTTP {0} {1}" -f [int]$resp.StatusCode, $resp.StatusDescription)
  }
  throw
}
