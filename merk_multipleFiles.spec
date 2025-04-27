# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['merk.py'],
    pathex=[''],
    binaries=[],
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
        ('merk/resources/resources.py','merk/resources'),

    ],
    hiddenimports=[],
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
    icon='merk.ico'
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
