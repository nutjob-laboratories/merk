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

# Format minor version so it is always
# at least three digits long
if len(minor)==1:
	minor = f"00{minor}"
elif len(minor)==2:
	minor = f"0{minor}"

f = open("./merk/data/win_minor.txt","w")
f.write(minor)
f.close()

f = open("merk_setup.txt","r")
setup = f.read()
f.close()

setup = setup.replace("!_WIN_VERSION_!",major+"."+minor)

f = open("merk_setup.iss","w")
f.write(setup)
f.close()

os.system("make_multiple.bat")

archive_name = f"merk-windows-{major}.zip"

os.rename('merk.zip', archive_name)

shutil.copy(archive_name, f"./downloads/merk-windows-{major}.{minor}.zip")

if os.path.isfile(f"./downloads/merk-windows-latest.zip"): os.remove("./downloads/merk-windows-latest.zip")

shutil.copy(archive_name, "./downloads/merk-windows-latest.zip")

os.remove(archive_name)

# os.system("make_single.bat")

# archive_name = f"merk-windows-standalone.zip"

# if os.path.isfile(f"./downloads/{archive_name}"): os.remove(f"./downloads/{archive_name}")

# shutil.copy(archive_name, "./downloads/"+archive_name)

# shutil.copy(archive_name, "./downloads/"+f"merk-windows-standalone-{major}.{minor}.zip")

# os.remove(archive_name)

shutil.copy("merk_setup.zip", f"./downloads/merk_setup-{major}.{minor}.zip")

if os.path.isfile(f"./downloads/merk_setup.zip"): os.remove(f"./downloads/merk_setup.zip")

shutil.copy("merk_setup.zip", "./downloads/merk_setup.zip")

os.remove("merk_setup.zip")
os.remove("setup.exe")
# os.remove("merk.exe")