Param(
  [string]$Identifier = "lead-acc-123",
  [string]$Name = "Alice Account",
  [string]$Email = "alice.account@acme.com",
  [string]$Message = "Olá, mensagem via Account API",
  [string]$Chatwoot = $env:CHATWOOT_BASE_URL,
  [string]$AccountId = $env:CHATWOOT_ACCOUNT_ID,
  [string]$AccessToken = $env:CHATWOOT_ACCESS_TOKEN,
  [int]$InboxId
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
if (-not $Chatwoot -or -not $AccountId -or -not $AccessToken) {
  $envPath = [System.IO.Path]::Combine($PSScriptRoot, '..', '.env')
  $envMap = Get-DotEnvValues -Path $envPath
  if (-not $Chatwoot -and $envMap.ContainsKey('CHATWOOT_BASE_URL')) { $Chatwoot = $envMap['CHATWOOT_BASE_URL'] }
  if (-not $AccountId -and $envMap.ContainsKey('CHATWOOT_ACCOUNT_ID')) { $AccountId = $envMap['CHATWOOT_ACCOUNT_ID'] }
  if (-not $AccessToken -and $envMap.ContainsKey('CHATWOOT_ACCESS_TOKEN')) { $AccessToken = $envMap['CHATWOOT_ACCESS_TOKEN'] }
}

if (-not $Chatwoot) { throw "CHATWOOT_BASE_URL is required" }
if (-not $AccountId) { throw "CHATWOOT_ACCOUNT_ID is required" }
if (-not $AccessToken) { throw "CHATWOOT_ACCESS_TOKEN is required" }

$base = $Chatwoot.TrimEnd('/')
$headers = @{ 'Content-Type' = 'application/json'; 'Authorization' = "Bearer $AccessToken" }

Write-Host "Using Chatwoot: $base (account $AccountId)" -ForegroundColor Cyan

try {
  # Discover Inbox numeric id if not provided
  if (-not $InboxId) {
    $urlInbox = "$base/api/v1/accounts/$AccountId/inboxes"
    $respInbox = Invoke-RestMethod -Method Get -Uri $urlInbox -Headers $headers
    # Try matching with CHATWOOT_INBOX_ID if present in .env (public identifier)
    $envPath = [System.IO.Path]::Combine($PSScriptRoot, '..', '.env')
    $envMap = Get-DotEnvValues -Path $envPath
    $publicId = if ($envMap.ContainsKey('CHATWOOT_INBOX_ID')) { $envMap['CHATWOOT_INBOX_ID'] } else { $null }
    $candidate = $null
    if ($publicId) {
      foreach ($it in $respInbox) {
        if ($it.PSObject.Properties.Name -contains 'identifier' -and $it.identifier -eq $publicId) { $candidate = $it; break }
        if ($it.PSObject.Properties.Name -contains 'inbox_identifier' -and $it.inbox_identifier -eq $publicId) { $candidate = $it; break }
        if ($it.PSObject.Properties.Name -contains 'website_token' -and $it.website_token -eq $publicId) { $candidate = $it; break }
      }
    }
    if (-not $candidate) { $candidate = ($respInbox | Select-Object -First 1) }
    if (-not $candidate -or -not ($candidate.PSObject.Properties.Name -contains 'id')) {
      throw "Failed to resolve Inbox numeric id from /inboxes response: $($respInbox | ConvertTo-Json -Depth 6)"
    }
    $InboxId = [int]$candidate.id
  }
  Write-Host ("InboxId={0}" -f $InboxId) -ForegroundColor Green

  # 1) Create contact (Account API)
  $contactBody = @{ identifier = $Identifier; name = $Name; email = $Email } | ConvertTo-Json -Depth 5
  $url1 = "$base/api/v1/accounts/$AccountId/contacts"
  $resp1 = Invoke-RestMethod -Method Post -Uri $url1 -Headers $headers -Body $contactBody
  $CONTACT_ID = $null
  if ($resp1.PSObject.Properties.Name -contains 'id') { $CONTACT_ID = $resp1.id }
  elseif ($resp1.PSObject.Properties.Name -contains 'contact' -and $resp1.contact.id) { $CONTACT_ID = $resp1.contact.id }
  if (-not $CONTACT_ID) { throw "Failed to obtain CONTACT_ID from response: $($resp1 | ConvertTo-Json -Depth 8)" }
  Write-Host ("CONTACT_ID={0}" -f $CONTACT_ID) -ForegroundColor Green

  # 2) Create conversation (Account API) for contact in the chosen inbox
  $convBody = @{ inbox_id = $InboxId } | ConvertTo-Json -Depth 3
  $url2 = "$base/api/v1/accounts/$AccountId/contacts/$CONTACT_ID/conversations"
  $resp2 = Invoke-RestMethod -Method Post -Uri $url2 -Headers $headers -Body $convBody
  $CVID = $null
  if ($resp2.PSObject.Properties.Name -contains 'id') { $CVID = $resp2.id }
  elseif ($resp2.PSObject.Properties.Name -contains 'conversation' -and $resp2.conversation.id) { $CVID = $resp2.conversation.id }
  if (-not $CVID) { throw "Failed to obtain conversation id from response: $($resp2 | ConvertTo-Json -Depth 8)" }
  Write-Host ("CVID={0}" -f $CVID) -ForegroundColor Green

  # 3) Send outgoing message (Account API)
  $msgBody = @{ content = $Message; message_type = 'outgoing'; private = $false } | ConvertTo-Json -Depth 5
  $url3 = "$base/api/v1/accounts/$AccountId/conversations/$CVID/messages"
  $resp3 = Invoke-RestMethod -Method Post -Uri $url3 -Headers $headers -Body $msgBody
  $MID = $null
  if ($resp3.PSObject.Properties.Name -contains 'id') { $MID = $resp3.id }
  elseif ($resp3.PSObject.Properties.Name -contains 'message' -and $resp3.message.id) { $MID = $resp3.message.id }
  if (-not $MID) { throw "Failed to obtain message id from response: $($resp3 | ConvertTo-Json -Depth 8)" }
  Write-Host ("MESSAGE_ID={0}" -f $MID) -ForegroundColor Green

  # Summary
  Write-Output ("CONTACT_ID={0}" -f $CONTACT_ID)
  Write-Output ("CVID={0}" -f $CVID)
  Write-Output ("MESSAGE_ID={0}" -f $MID)

} catch {
  Write-Error "Chatwoot Account API demo failed: $($_.Exception.Message)"
  if ($_.Exception.Response -and ($_.Exception.Response -is [System.Net.HttpWebResponse])) {
    $resp = $_.Exception.Response
    Write-Error ("HTTP {0} {1}" -f [int]$resp.StatusCode, $resp.StatusDescription)
  }
  throw
}

