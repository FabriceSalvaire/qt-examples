# Copyright (C) 2022 The Qt Company Ltd.
# SPDX-License-Identifier: LicenseRef-Qt-Commercial OR BSD-3-Clause

"""
hello_app.spec

This is almost the spec file generated by running PyInstaller.
Just the paths were adjusted and made relative.
As an effect, all the analysis is avoided, and the log file of
wheel_tester.py went down from 775 lines to 278 lines. :-)
"""

block_cipher = None


a = Analysis(['hello.py'],
             pathex=['pyinstaller'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             # 2019-04-28
             # This hack circumvents a side effect of Python 2.7.16 which leads to a failure
             # in 'hook-_tkinter.py'. The error is reported. Until it is fixed, we circumvent
             # the problem by this exclude.
             # This effect is triggered by installing 'numpy'. It is somewhat special since
             # the problem does not show up in Python 3.7 . tkinter would have the same
             # problem on Python 3.7, but numpy would not trigger it for some reason.
             excludes=['FixTk', 'tcl', 'tk', '_tkinter', 'tkinter', 'Tkinter'],
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
          name='hello_app',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='hello_app')