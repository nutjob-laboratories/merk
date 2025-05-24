pyinstaller merk_singleFile.spec
move .\dist\merk.exe .\merk.exe
powershell.exe -noprofile -command "Compress-Archive -Path \"merk.exe\" -DestinationPath \"merk-windows-standalone.zip\""
rmdir /s /q build
rmdir /s /q dist