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

# Format minor version so it is always
# at least three digits long
if len(minor)==1:
	minor = f"00{minor}"
elif len(minor)==2:
	minor = f"0{minor}"

f = open("./merk/data/minor.txt","w")
f.write(minor)
f.close()

# Write version to python file to be loaded in
f = open("./merk/resources/version.py","w")
f.write(f"APPLICATION_VERSION = \"{major}.{minor}\"")
f.close()

# Format minor version so it is always
# at least three digits long
if len(minor)==1:
	minor = f"00{minor}"
elif len(minor)==2:
	minor = f"0{minor}"

f = open("./merk/data/win_major.txt","r")
win_major = f.read()
f.close()

f = open("./merk/data/win_minor.txt","r")
win_minor = f.read()
f.close()

# Build README

x = open("README.txt",mode="r", encoding='latin-1')
readme = str(x.read())
x.close()

readme = readme.replace("!_VERSION_!",major)
readme = readme.replace("!_MINOR_!",minor)
readme = readme.replace("!_FULL_VERSION_!",major+"."+minor)
readme = readme.replace("!_WIN_VERSION_!",win_major+"."+win_minor)

os.remove("README.md")
f = open("README.md",mode="w", encoding='latin-1')
f.write(readme)
f.close()

# Build distribution zips

os.mkdir("./dist")

shutil.copytree("./merk", "./dist/merk",ignore=shutil.ignore_patterns('*.pyc', 'tmp*',"__pycache__"))
shutil.copytree("./qt5reactor", "./dist/qt5reactor",ignore=shutil.ignore_patterns('*.pyc', 'tmp*',"__pycache__"))
shutil.copytree("./spellchecker", "./dist/spellchecker",ignore=shutil.ignore_patterns('*.pyc', 'tmp*',"__pycache__"))
shutil.copytree("./emoji", "./dist/emoji",ignore=shutil.ignore_patterns('*.pyc', 'tmp*',"__pycache__"))

shutil.copy("./merk.py", "./dist/merk.py")
shutil.copy("./LICENSE", "./dist/LICENSE")
shutil.copy("./merk.ico", "./dist/merk.ico")

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