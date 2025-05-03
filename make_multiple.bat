pyinstaller merk_multipleFiles.spec
powershell.exe -nologo -noprofile -command "& { Add-Type -A 'System.IO.Compression.FileSystem'; [IO.Compression.ZipFile]::CreateFromDirectory('dist\merk', 'merk.zip'); }"
iscc merk_setup.iss
move .\Output\merk_setup.exe .\merk_setup.exe
rmdir /s /q build
rmdir /s /q dist
rmdir /s /q Output
