pyinstaller merk_multipleFiles.spec

cd dist
cd merk
zip -r merk.zip ./*
mv merk.zip ../../
cd ..
cd ..

zip -u merk.zip README.html
zip -u merk.zip LICENSE
zip -u merk.zip CHANGELOG

mv merk.zip ./downloads/merk-linux-latest.zip
cp -f ./downloads/merk-linux-latest.zip /home/wraithnix/Dropbox/Public/merk-linux-latest.zip

rm -rf ./build
rm -rf ./dist
