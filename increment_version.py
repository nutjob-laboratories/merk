import os
import shutil
import sys
import platform

# Load and increment main version number

f = open("./merk/data/major.txt","r")
major = f.read()
f.close()

f = open("./merk/data/minor.txt","r")
minor = f.read()
f.close()

mi = int(minor)
mi = mi + 1
if mi>=1000: mi = 0
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

f = open("./merk/data/url.txt","r")
rurl = f.read()
f.close()

f = open("./merk/data/release.txt","r")
rversion = f.read()
f.close()

# Write version to python file to be loaded in
f = open("./merk/resources/release.py","w")
f.write(f"APPLICATION_RELEASE = \"{rurl}\"\nAPPLICATION_RELEASE_VERSION = \"{rversion}\"")
f.close()


f = open("./merk/data/win_major.txt","r")
major = f.read()
f.close()

f = open("./merk/data/win_minor.txt","r")
minor = f.read()
f.close()

mi = int(minor)
mi = mi + 1
if mi>=1000: mi = 0
minor = str(mi)

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

f = open("./merk/data/lin_major.txt","r")
major = f.read()
f.close()

f = open("./merk/data/lin_minor.txt","r")
minor = f.read()
f.close()

mi = int(minor)
mi = mi + 1
if mi>=1000: mi = 0
minor = str(mi)

# Format minor version so it is always
# at least three digits long
if len(minor)==1:
	minor = f"00{minor}"
elif len(minor)==2:
	minor = f"0{minor}"

f = open("./merk/data/lin_minor.txt","w")
f.write(minor)
f.close()
