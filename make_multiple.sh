pyinstaller merk_wayland.spec

cd dist
cd merk
zip -r merk.zip ./*
mv merk.zip ../../
cd ..
cd ..

zip -u merk.zip README.html
zip -u merk.zip LICENSE
zip -u merk.zip CHANGELOG

cp -f merk.zip /home/wraithnix/Dropbox/Public/merk-linux-latest.zip

major_version=$(cat ./merk/data/major.txt)
minor_version=$(cat ./merk/data/minor.txt)
mv merk.zip "./downloads/merk-linux-$major_version-$minor_version.zip"

rm -rf ./build
rm -rf ./dist
