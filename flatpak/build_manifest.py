f = open("./manifest.yml","r")
manifest = f.read()
f.close()

f = open("./hash.txt","r")
fhash = f.read()
f.close()

fhash = fhash.strip()

manifest = manifest.replace("__HASH__",fhash)

f = open("merk.yml",mode="w", encoding='latin-1')
f.write(manifest)
f.close()
