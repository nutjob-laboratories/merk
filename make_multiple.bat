pyinstaller merk_multipleFiles.spec
powershell.exe -nologo -noprofile -command "& { Add-Type -A 'System.IO.Compression.FileSystem'; [IO.Compression.ZipFile]::CreateFromDirectory('dist\merk', 'merk.zip'); }"
rmdir /s /q build
rmdir /s /q dist