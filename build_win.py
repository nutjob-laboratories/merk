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

if os.path.isfile(f"./downloads/merk-windows-latest.zip"): os.remove("./downloads/merk-windows-latest.zip")

shutil.copy(archive_name, "./downloads/merk-windows-latest.zip")

os.remove(archive_name)

if os.path.isfile(f"./downloads/merk-windows-setup.zip"): os.remove(f"./downloads/merk-windows-setup.zip")

shutil.copy("merk-windows-setup.zip", "./downloads/merk-windows-setup.zip")

os.remove("merk-windows-setup.zip")
os.remove("setup.exe")
#os.remove("merk.exe")