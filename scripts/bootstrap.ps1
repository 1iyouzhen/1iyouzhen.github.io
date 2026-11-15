$ErrorActionPreference = 'Stop'
$ProgressPreference = 'SilentlyContinue'
$root = Split-Path $PSScriptRoot -Parent
$toolDir = Join-Path $root '.tools'
New-Item -ItemType Directory -Path $toolDir -Force | Out-Null
$headers = @{ 'User-Agent' = 'Youzhen-Blog-Builder' }
$release = Invoke-RestMethod -Uri 'https://api.github.com/repos/gohugoio/hugo/releases/tags/v0.170.0' -Headers $headers
$asset = $release.assets | Where-Object { $_.name -like 'hugo_extended_*windows-amd64.zip' } | Select-Object -First 1
if (-not $asset) { throw 'Hugo Windows asset missing' }
Invoke-WebRequest -Uri $asset.browser_download_url -OutFile (Join-Path $toolDir 'hugo.zip') -UseBasicParsing
$checks = $release.assets | Where-Object { $_.name -like '*checksums.txt' } | Select-Object -First 1
$response = Invoke-WebRequest -Uri $checks.browser_download_url -UseBasicParsing; $checkText = if ($response.Content -is [byte[]]) { [System.Text.Encoding]::UTF8.GetString($response.Content) } else { [string]$response.Content }
$expected = (($checkText -split [char]10 | Where-Object { $_ -like ('*' + $asset.name) }) -split '\s+')[0]
$actual = (Get-FileHash -LiteralPath (Join-Path $toolDir 'hugo.zip') -Algorithm SHA256).Hash
if ($expected.ToLowerInvariant() -ne $actual.ToLowerInvariant()) { throw 'Hugo checksum mismatch' }
Expand-Archive -LiteralPath (Join-Path $toolDir 'hugo.zip') -DestinationPath $toolDir -Force
& (Join-Path $toolDir 'hugo.exe') version
if (-not (Test-Path (Join-Path $root 'themes/PaperMod'))) {
  $commit = Invoke-RestMethod -Uri 'https://api.github.com/repos/adityatelange/hugo-PaperMod/commits/master' -Headers $headers
  Invoke-WebRequest -Uri ('https://codeload.github.com/adityatelange/hugo-PaperMod/zip/' + $commit.sha) -OutFile (Join-Path $toolDir 'papermod.zip') -UseBasicParsing
  Expand-Archive -LiteralPath (Join-Path $toolDir 'papermod.zip') -DestinationPath $toolDir -Force
  New-Item -ItemType Directory -Path (Join-Path $root 'themes') -Force | Out-Null
  Copy-Item -LiteralPath (Join-Path $toolDir ('hugo-PaperMod-' + $commit.sha)) -Destination (Join-Path $root 'themes/PaperMod') -Recurse
  @{ hugo = '0.170.0'; hugosha256 = $actual.ToLowerInvariant(); theme = 'PaperMod'; themecommit = $commit.sha; themeurl = 'https://github.com/adityatelange/hugo-PaperMod' } | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $root 'versions.json') -Encoding UTF8
}
Get-Content -LiteralPath (Join-Path $root 'versions.json') -Encoding UTF8
