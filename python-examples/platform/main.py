#  Copyright (C) 2022 Fabrice Salvaire
#  SPDX-License-Identifier: BSD-3-Clause

####################################################################################################

import sys

from PySide6.QtGui import QGuiApplication

####################################################################################################

import os
os.environ['QT_LOGGING_RULES'] = ';'.join((
    '*.debug=true',
    'qt.*.debug=false',
    '*.info=true',
))

####################################################################################################

if __name__ == '__main__':
    app = QGuiApplication(sys.argv)

    print('Platform:', app.platformName())

    # https://doc.qt.io/qt-6/qscreen.html
    # screen = app.primaryScreen()
    for screen in app.screens():
        print('Screen:', screen.name())
        _ = screen.size()
        print(f'    size [px]: {_.width()} x {_.height()}')
        _ = screen.physicalSize()
        print(f'    size [mm]: {_.width()} x {_.height()}')
        print(f'    DPI: {screen.physicalDotsPerInch():.1f}')
        print(f'    device pixel ratio: {screen.devicePixelRatio()}')
        print(f'    orientation: {screen.primaryOrientation()}')
        print(f'    depth: {screen.depth()}')
