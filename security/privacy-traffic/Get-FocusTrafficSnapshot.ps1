param(
  [string]$OutDir = "D:\TheFocusFiles\FOCUS_MASTER_AI_live\security\privacy-traffic\snapshots"
)
New-Item -ItemType Directory -Force -Path $OutDir | Out-Null
$stamp = Get-Date -Format "yyyyMMdd-HHmmss"
$tcp = Get-NetTCPConnection -ErrorAction SilentlyContinue | Select-Object LocalAddress,LocalPort,RemoteAddress,RemotePort,State,OwningProcess
$proc = Get-Process | Select-Object Id,ProcessName,Path
$dns = Get-DnsClientCache -ErrorAction SilentlyContinue | Select-Object Entry,Name,Type,Data,Status
$routes = Get-NetRoute -ErrorAction SilentlyContinue | Select-Object DestinationPrefix,NextHop,InterfaceAlias,RouteMetric
$startup = Get-CimInstance Win32_StartupCommand -ErrorAction SilentlyContinue | Select-Object Name,Command,Location,User
$tcp | Export-Csv -NoTypeInformation -Path (Join-Path $OutDir "$stamp-tcp.csv")
$proc | Export-Csv -NoTypeInformation -Path (Join-Path $OutDir "$stamp-processes.csv")
$dns | Export-Csv -NoTypeInformation -Path (Join-Path $OutDir "$stamp-dns-cache.csv")
$routes | Export-Csv -NoTypeInformation -Path (Join-Path $OutDir "$stamp-routes.csv")
$startup | Export-Csv -NoTypeInformation -Path (Join-Path $OutDir "$stamp-startup.csv")
Write-Host "Traffic snapshot written to $OutDir with timestamp $stamp"
