import os
import shutil
import sys
import platform

# Compile resources
devp = platform.system()
if "Windows" in devp:
	os.system("compile_resources.bat")
elif "Linux" in devp:
	os.system("sh compile_resources.sh")
else:
	print("This platform is not supported")
	sys.exit(1)

# Load and increment version numbers

f = open("./merk/data/major.txt","r")
major = f.read()
f.close()

f = open("./merk/data/minor.txt","r")
minor = f.read()
f.close()

mi = int(minor)
mi = mi + 1
minor = str(mi)

f = open("./merk/data/minor.txt","w")
f.write(minor)
f.close()

# Format minor version so it is always
# at least three digits long
if len(minor)==1:
	minor = f"00{minor}"
elif len(minor)==2:
	minor = f"0{minor}"

# Build distribution zips

os.mkdir("./dist")

shutil.copytree("./merk", "./dist/merk",ignore=shutil.ignore_patterns('*.pyc', 'tmp*',"__pycache__"))
shutil.copytree("./qt5reactor", "./dist/qt5reactor",ignore=shutil.ignore_patterns('*.pyc', 'tmp*',"__pycache__"))

shutil.copy("./merk.py", "./dist/merk.py")
shutil.copy("./LICENSE", "./dist/LICENSE")
shutil.copy("./README.md", "./dist/README.md")

if "Windows" in devp:
	os.system("powershell.exe -nologo -noprofile -command \"& { Add-Type -A 'System.IO.Compression.FileSystem'; [IO.Compression.ZipFile]::CreateFromDirectory('dist', 'dist.zip'); }\" ")
elif "Linux" in devp:
	os.system("cd dist; zip -r ../dist.zip . ; cd ..")

shutil.rmtree('./dist')

archive_name = f"merk-{major}.zip"

os.rename('dist.zip', archive_name)

if os.path.isfile(f"./downloads/{archive_name}"): os.remove(f"./downloads/{archive_name}")
if os.path.isfile(f"./downloads/merk-latest.zip"): os.remove("./downloads/merk-latest.zip")

shutil.copy(archive_name, "./downloads/"+archive_name)
shutil.copy(archive_name, "./downloads/merk-latest.zip")

os.remove(archive_name)