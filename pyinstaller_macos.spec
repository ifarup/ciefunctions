# -*- mode: python -*-

block_cipher = None


a = Analysis(['ciefunctions.py'],
             pathex=['/Users/sjg/TEMP/ciefunctions'],
             binaries=[],
             datas=[('tc1_97/data', 'tc1_97/data'),
                    ('tc1_97/*.css', 'tc1_97'),
                    ('web', 'web')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [('u', None, 'OPTION')],
          exclude_binaries=True,
          name='ciefunctions',
          debug=False,
          strip=False,
          upx=True,
          console=False )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='ciefunctions')
app = BUNDLE(coll,
             name='ciefunctions.app',
             icon='ciefunctions.icns',
             info_plist={'NSHighResolutionCapable': 'True'},
             bundle_identifier='org.qt-project.Qt.QtWebEngineCore')
