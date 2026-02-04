import os
import sys
import sysconfig
from PyInstaller.utils.hooks import collect_submodules

sys_qt_plugins = '/usr/lib/x86_64-linux-gnu/qt5/plugins' 

def collect_plugin_dir(source_subdir, dest_subdir):
    full_path = os.path.join(sys_qt_plugins, source_subdir)
    binaries = []
    if os.path.exists(full_path):
        for f in os.listdir(full_path):
            if f.endswith('.so'):
                binaries.append((os.path.join(full_path, f), os.path.join('qt5_plugins', dest_subdir)))
    return binaries

# Collect the binaries
found_binaries = []
found_binaries += collect_plugin_dir('platforms', 'platforms')
found_binaries += collect_plugin_dir('wayland-graphics-integration', 'wayland-graphics-integration')

a = Analysis(
    ['merk.py'],
    pathex=[''],
    binaries=found_binaries,
    datas=[
        ('emoji/unicode_codes/emoji.json','emoji/unicode_codes'),
        ('emoji/unicode_codes/emoji_ar.json','emoji/unicode_codes'),
        ('emoji/unicode_codes/emoji_de.json','emoji/unicode_codes'),
        ('emoji/unicode_codes/emoji_es.json','emoji/unicode_codes'),
        ('emoji/unicode_codes/emoji_fa.json','emoji/unicode_codes'),
        ('emoji/unicode_codes/emoji_fr.json','emoji/unicode_codes'),
        ('emoji/unicode_codes/emoji_id.json','emoji/unicode_codes'),
        ('emoji/unicode_codes/emoji_it.json','emoji/unicode_codes'),
        ('emoji/unicode_codes/emoji_ja.json','emoji/unicode_codes'),
        ('emoji/unicode_codes/emoji_ko.json','emoji/unicode_codes'),
        ('emoji/unicode_codes/emoji_pt.json','emoji/unicode_codes'),
        ('emoji/unicode_codes/emoji_ru.json','emoji/unicode_codes'),
        ('emoji/unicode_codes/emoji_tr.json','emoji/unicode_codes'),
        ('emoji/unicode_codes/emoji_zh.json','emoji/unicode_codes'),
        ('spellchecker/resources/de.json.gz','spellchecker/resources'),
        ('spellchecker/resources/en.json.gz','spellchecker/resources'),
        ('spellchecker/resources/es.json.gz','spellchecker/resources'),
        ('spellchecker/resources/fr.json.gz','spellchecker/resources'),
        ('spellchecker/resources/pt.json.gz','spellchecker/resources'),
        ('spellchecker/resources/ar.json.gz','spellchecker/resources'),
        ('spellchecker/resources/eu.json.gz','spellchecker/resources'),
        ('spellchecker/resources/fa.json.gz','spellchecker/resources'),
        ('spellchecker/resources/it.json.gz','spellchecker/resources'),
        ('spellchecker/resources/lv.json.gz','spellchecker/resources'),
        ('spellchecker/resources/nl.json.gz','spellchecker/resources'),
        ('spellchecker/resources/ru.json.gz','spellchecker/resources'),
        ('merk/resources/resources.py','merk/resources'),
        ('merk/resources/README.html','merk/resources'),
        ('merk/resources/rfc1459.pdf','merk/resources'),
        ('merk/resources/rfc2812.pdf','merk/resources'),
        ('merk/resources/emoji_shortcode_list.pdf','merk/resources'),
        ('merk/resources/MERK_User_Guide.pdf','merk/resources'),


    ],
    hiddenimports=collect_submodules('PyQt5') + ['PyQt5.QtMultimedia'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='merk',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=True,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='merk.ico',
    contents_directory='lib',
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='merk',
)
