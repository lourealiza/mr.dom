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
$headers = @{ 'Content-Type' = 'application/json'; 'api_access_token' = $AccessToken }

Write-Host "Using Chatwoot: $base (account $AccountId)" -ForegroundColor Cyan

try {
  # Discover Inbox numeric id if not provided
  if (-not $InboxId) {
    $urlInbox = "$base/api/v1/accounts/$AccountId/inboxes"
    $respInbox = Invoke-RestMethod -Method Get -Uri $urlInbox -Headers $headers
    # Normalize response: some Chatwoot versions return { payload: [...] }
    $list = $respInbox
    if ($respInbox -and ($respInbox.PSObject.Properties.Name -contains 'payload')) { $list = $respInbox.payload }
    # Try matching with CHATWOOT_INBOX_ID if present in .env (public identifier)
    $envPath = [System.IO.Path]::Combine($PSScriptRoot, '..', '.env')
    $envMap = Get-DotEnvValues -Path $envPath
    $publicId = if ($envMap.ContainsKey('CHATWOOT_INBOX_ID')) { $envMap['CHATWOOT_INBOX_ID'] } else { $null }
    $candidate = $null
    if ($publicId) {
      foreach ($it in $list) {
        if ($it.PSObject.Properties.Name -contains 'identifier' -and $it.identifier -eq $publicId) { $candidate = $it; break }
        if ($it.PSObject.Properties.Name -contains 'inbox_identifier' -and $it.inbox_identifier -eq $publicId) { $candidate = $it; break }
        if ($it.PSObject.Properties.Name -contains 'website_token' -and $it.website_token -eq $publicId) { $candidate = $it; break }
      }
    }
    if (-not $candidate) { $candidate = ($list | Select-Object -First 1) }
    if (-not $candidate -or -not ($candidate.PSObject.Properties.Name -contains 'id')) {
      throw "Failed to resolve Inbox numeric id from /inboxes response: $($respInbox | ConvertTo-Json -Depth 6)"
    }
    $InboxId = [int]$candidate.id
  }
  Write-Host ("InboxId={0}" -f $InboxId) -ForegroundColor Green

  # 1) Create contact (Account API)
  $contactBody = @{ identifier = $Identifier; name = $Name; email = $Email } | ConvertTo-Json -Depth 5
  $url1 = "$base/api/v1/accounts/$AccountId/contacts"
  $resp1 = $null
  try {
    $resp1 = Invoke-RestMethod -Method Post -Uri $url1 -Headers $headers -Body $contactBody
  } catch {
    Write-Warning "Create contact failed (trying to resolve existing): $($_.Exception.Message)"
    if ($_.Exception.Response) {
      $sr = New-Object IO.StreamReader($_.Exception.Response.GetResponseStream()); $bodyErr = $sr.ReadToEnd(); Write-Warning $bodyErr
    }
    # Try search by identifier/email
    $urlSearch = "$base/api/v1/accounts/$AccountId/contacts/search?q=$([uri]::EscapeDataString($Identifier))"
    try {
      $respSearch = Invoke-RestMethod -Method Get -Uri $urlSearch -Headers $headers
      if ($respSearch -and ($respSearch.PSObject.Properties.Name -contains 'payload')) { $respSearch = $respSearch.payload }
      if ($respSearch -and $respSearch.contacts) { $resp1 = @{ contact = ($respSearch.contacts | Select-Object -First 1) } }
    } catch { Write-Warning "Search by identifier failed: $($_.Exception.Message)" }
    if (-not $resp1) {
      $urlQ = "$base/api/v1/accounts/$AccountId/contacts/search?q=$([uri]::EscapeDataString($Email))"
      try {
        $respSearch2 = Invoke-RestMethod -Method Get -Uri $urlQ -Headers $headers
        if ($respSearch2 -and ($respSearch2.PSObject.Properties.Name -contains 'payload')) { $respSearch2 = $respSearch2.payload }
        if ($respSearch2 -and $respSearch2.contacts) { $resp1 = @{ contact = ($respSearch2.contacts | Select-Object -First 1) } }
      } catch { Write-Warning "Search by email failed: $($_.Exception.Message)" }
    }
    if (-not $resp1) { throw }
  }
  # Normalize payload wrapper
  $r1 = $resp1
  if ($resp1 -and ($resp1.PSObject.Properties.Name -contains 'payload')) { $r1 = $resp1.payload }
  $CONTACT_ID = $null
  if ($r1.PSObject.Properties.Name -contains 'id') { $CONTACT_ID = $r1.id }
  elseif ($r1.PSObject.Properties.Name -contains 'contact' -and $r1.contact.id) { $CONTACT_ID = $r1.contact.id }
  if (-not $CONTACT_ID) { throw "Failed to obtain CONTACT_ID from response: $($resp1 | ConvertTo-Json -Depth 8)" }
  Write-Host ("CONTACT_ID={0}" -f $CONTACT_ID) -ForegroundColor Green

  # 2) Ensure contact is linked to inbox (contact_inboxes) for Channel::Api
  $sourceId = [guid]::NewGuid().ToString()
  $url1b = "$base/api/v1/accounts/$AccountId/contacts/$CONTACT_ID/contact_inboxes"
  $body1b = @{ inbox_id = $InboxId; source_id = $sourceId } | ConvertTo-Json -Depth 4
  try {
    $resp1b = Invoke-RestMethod -Method Post -Uri $url1b -Headers $headers -Body $body1b
  } catch {
    # If already exists, continue; otherwise log
    Write-Warning "contact_inboxes link may already exist: $($_.Exception.Message)"
  }

  # 3) Create conversation for contact in the chosen inbox
  $convBody = @{ inbox_id = $InboxId } | ConvertTo-Json -Depth 3
  $url2 = "$base/api/v1/accounts/$AccountId/contacts/$CONTACT_ID/conversations"
  try {
    $resp2 = Invoke-RestMethod -Method Post -Uri $url2 -Headers $headers -Body $convBody
  } catch {
    # Fallback: create via conversations root
    Write-Warning "Fallback to /conversations endpoint due to: $($_.Exception.Message)"
    $url2b = "$base/api/v1/accounts/$AccountId/conversations"
    $body2b = @{ inbox_id = $InboxId; contact_id = $CONTACT_ID; source_id = $sourceId } | ConvertTo-Json -Depth 4
    try {
      $resp2 = Invoke-RestMethod -Method Post -Uri $url2b -Headers $headers -Body $body2b
    } catch {
      Write-Error "Create conversation failed: $($_.Exception.Message)"
      if ($_.Exception.Response) { $sr = New-Object IO.StreamReader($_.Exception.Response.GetResponseStream()); Write-Error ($sr.ReadToEnd()) }
      throw
    }
  }
  $r2 = $resp2
  if ($resp2 -and ($resp2.PSObject.Properties.Name -contains 'payload')) { $r2 = $resp2.payload }
  $CVID = $null
  if ($r2.PSObject.Properties.Name -contains 'id') { $CVID = $r2.id }
  elseif ($r2.PSObject.Properties.Name -contains 'conversation' -and $r2.conversation.id) { $CVID = $r2.conversation.id }
  if (-not $CVID) { throw "Failed to obtain conversation id from response: $($resp2 | ConvertTo-Json -Depth 8)" }
  Write-Host ("CVID={0}" -f $CVID) -ForegroundColor Green

  # 4) Send outgoing message (Account API)
  $msgBody = @{ content = $Message; message_type = 'outgoing'; private = $false } | ConvertTo-Json -Depth 5
  $url3 = "$base/api/v1/accounts/$AccountId/conversations/$CVID/messages"
  try {
    $resp3 = Invoke-RestMethod -Method Post -Uri $url3 -Headers $headers -Body $msgBody
  } catch {
    Write-Error "Send message failed: $($_.Exception.Message)"
    if ($_.Exception.Response) { $sr = New-Object IO.StreamReader($_.Exception.Response.GetResponseStream()); Write-Error ($sr.ReadToEnd()) }
    throw
  }
  $r3 = $resp3
  if ($resp3 -and ($resp3.PSObject.Properties.Name -contains 'payload')) { $r3 = $resp3.payload }
  $MID = $null
  if ($r3.PSObject.Properties.Name -contains 'id') { $MID = $r3.id }
  elseif ($r3.PSObject.Properties.Name -contains 'message' -and $r3.message.id) { $MID = $r3.message.id }
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
