import os

# Load and increment version numbers

f = open("./merk/data/major.txt","r")
major = f.read()
f.close()

f = open("./merk/data/minor.txt","r")
minor = f.read()
f.close()

# Build README

x = open("README.txt",mode="r", encoding='latin-1')
readme = str(x.read())
x.close()

readme = readme.replace("!_VERSION_!",major)
readme = readme.replace("!_MINOR_!",minor)
readme = readme.replace("!_FULL_VERSION_!",major+"."+minor)

os.remove("README.md")
f = open("README.md",mode="w", encoding='latin-1')
f.write(readme)
f.close()
