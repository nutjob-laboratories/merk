pyinstaller merk_multipleFiles.spec
powershell.exe -nologo -noprofile -command "& { Add-Type -A 'System.IO.Compression.FileSystem'; [IO.Compression.ZipFile]::CreateFromDirectory('dist\merk', 'merk.zip'); }"
powershell -Command "Compress-Archive -Path 'README.html' -Update -DestinationPath 'merk.zip'"
iscc merk_setup.iss
move .\Output\merk_setup.exe .\setup.exe
powershell.exe -noprofile -command "Compress-Archive -Path \"setup.exe\" -DestinationPath \"merk_setup.zip\""
powershell -Command "Compress-Archive -Path 'README.html' -Update -DestinationPath 'merk_setup.zip'"
rmdir /s /q build
rmdir /s /q dist
rmdir /s /q Output
