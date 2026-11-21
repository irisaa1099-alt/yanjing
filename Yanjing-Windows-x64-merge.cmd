@echo off
setlocal
pushd "%~dp0" || exit /b 1
powershell.exe -NoProfile -Command "$ErrorActionPreference='Stop'; $out='Yanjing-Windows-x64.zip'; if(Test-Path -LiteralPath $out){throw ('Already exists: '+$out)}; $tmp=[IO.Path]::GetRandomFileName(); try { $dest=[IO.File]::Open($tmp,'CreateNew','Write','None'); try { 1..9 | ForEach-Object { $part=$out+'.'+$_.ToString('000'); $src=[IO.File]::OpenRead((Join-Path (Get-Location) $part)); try { $src.CopyTo($dest) } finally { $src.Dispose() } } } finally { $dest.Dispose() }; $sha=[Security.Cryptography.SHA256]::Create(); try { $stream=[IO.File]::OpenRead($tmp); try { $digest=[BitConverter]::ToString($sha.ComputeHash($stream)).Replace('-','') } finally { $stream.Dispose() } } finally { $sha.Dispose() }; if($digest -ne 'd87933338c84e75047385e1258711a767d9aeb7868485f3571c7ee4f1542031e'){throw 'SHA-256 mismatch. Download the parts again.'}; [IO.File]::Move($tmp,$out); Write-Host ('Verified '+$out) } finally { if(Test-Path -LiteralPath $tmp){Remove-Item -LiteralPath $tmp} }"
set "rc=%errorlevel%"
if not "%rc%"=="0" pause
popd
exit /b %rc%
