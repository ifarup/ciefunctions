# -*- mode: python -*-

block_cipher = None


a = Analysis(['ciefunctions.py'],
             pathex=['/home/ifarup/projects/tc1-97/ciefunctions'],
             binaries=[],
             datas=[('tc1_97/data', 'tc1_97/data'),
                    ('tc1_97/*.css', 'tc1_97'),
                    ('tc1_97/MathJax-2.7.5', 'tc1_97/MathJax-2.7.5'),
                    ('tc1_97/icons', 'tc1_97/icons')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
          cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='ciefunctions',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='ciefunctions',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True )
