# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['orac2csv.py'],
             pathex=['E:\\9月\\nsw.md.go.th-海事处办公\\PYCC'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
a.binaries = a.binaries + [('oci.dll', 'E:\\oci.dll','BINARY')]

a.binaries = a.binaries + [('oraocci11.dll', 'E:\\oraocci11.dll','BINARY')]

a.binaries = a.binaries + [('oraociei11.dll', 'E:\\oraociei11.dll','BINARY')]

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

			 
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,  
          [],
          name='orac2csv',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None )
