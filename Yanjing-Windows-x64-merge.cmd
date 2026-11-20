@echo off
setlocal
pushd "%~dp0" || exit /b 1
powershell.exe -NoProfile -Command "$ErrorActionPreference='Stop'; $out='Yanjing-Windows-x64.zip'; if(Test-Path -LiteralPath $out){throw ('Already exists: '+$out)}; $tmp=[IO.Path]::GetRandomFileName(); try { $dest=[IO.File]::Open($tmp,'CreateNew','Write','None'); try { 1..9 | ForEach-Object { $part=$out+'.'+$_.ToString('000'); $src=[IO.File]::OpenRead((Join-Path (Get-Location) $part)); try { $src.CopyTo($dest) } finally { $src.Dispose() } } } finally { $dest.Dispose() }; if((Get-FileHash -LiteralPath $tmp -Algorithm SHA256).Hash -ne '4482b3c8ed9f2c7130c9a3309d439887af6e6b9605ee6d7c58f4d25209bb6687'){throw 'SHA-256 mismatch. Download the parts again.'}; [IO.File]::Move($tmp,$out); Write-Host ('Verified '+$out) } finally { if(Test-Path -LiteralPath $tmp){Remove-Item -LiteralPath $tmp} }"
set "rc=%errorlevel%"
if not "%rc%"=="0" pause
popd
exit /b %rc%
