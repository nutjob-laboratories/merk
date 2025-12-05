import os
import shutil
import sys
import platform

# Load and increment version numbers

f = open("./merk/data/win_major.txt","r")
major = f.read()
f.close()

f = open("./merk/data/win_minor.txt","r")
minor = f.read()
f.close()

os.system("make_multiple.bat")

archive_name = f"merk-windows-{major}.zip"

os.rename('merk.zip', archive_name)

shutil.copy(archive_name, f"./downloads/merk-windows-{major}-{minor}.zip")

os.remove(archive_name)

shutil.copy("merk-windows-setup.zip", f"./downloads/merk-windows-setup-{major}-{minor}.zip")

os.remove("merk-windows-setup.zip")
os.remove("setup.exe")
