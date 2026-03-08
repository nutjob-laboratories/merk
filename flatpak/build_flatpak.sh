sha256sum /home/wraithnix/Dropbox/Public/merk-linux-latest.zip | cut -d ' ' -f 1 > hash.txt
python build_manifest.py
flatpak-builder --force-clean --repo=my-repo build-dir merk.yml 
flatpak build-bundle my-repo merk-latest.flatpak net.nutjob.Merk
rm merk.yml
rm hash.txt
rm -rf build-dir
rm -rf my-repo
rm -rf .flatpak-builder
mv -f merk-latest.flatpak /home/wraithnix/Dropbox/Public/merk-latest.flatpak

