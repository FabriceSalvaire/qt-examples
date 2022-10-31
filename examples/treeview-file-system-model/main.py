#  Copyright (C) 2022 Fabrice Salvaire
#  SPDX-License-Identifier: BSD-3-Clause

####################################################################################################

from pathlib import Path
import sys

from PySide6.QtCore import QAbstractListModel, Qt, QUrl, QDir
from PySide6.QtGui import QGuiApplication
from PySide6.QtQuick import QQuickView
from PySide6.QtQml import QQmlContext

# https://doc.qt.io/qt-6/qfilesystemmodel.html
# QtGui ???
from PySide6.QtWidgets import QFileSystemModel

####################################################################################################

import os
os.environ['QT_LOGGING_RULES'] = ';'.join((
    '*.debug=true',
    'qt.*.debug=false',
    '*.info=true',
))

####################################################################################################

class CustomCode:
    def __init__(self, context: QQmlContext) -> None:
        self._model = model = QFileSystemModel()
        model.setRootPath(QDir.currentPath())
        print('Model root path is', model.rootPath())
        root_path_index = model.index(model.rootPath())
        print('Number of rows', model.rowCount())
        print('Number of columns', model.columnCount())
        print('has children', model.hasChildren())
        # model.setFilter(QDir.AllEntries | QDir.AllDirs)
        print('Roles are')
        role_names = model.roleNames()
        for i in sorted(role_names):
            print(f'{role_names[i]}: {i}')

        context.setContextProperty('file_system_model', model)
        context.setContextProperty('root_path_index', root_path_index)

####################################################################################################

if __name__ == '__main__':
    app = QGuiApplication(sys.argv)
    view = QQuickView()
    context = view.rootContext()
    view.setResizeMode(QQuickView.SizeRootObjectToView)

    custom_code = CustomCode(context)

    qml_filename = 'view.qml'
    qml_path = Path(__file__).resolve().parent.joinpath(qml_filename)
    view.setSource(QUrl.fromLocalFile(qml_path))
    if view.status() == QQuickView.Error:
        sys.exit(-1)
    view.show()

    rc = app.exec()
    # Deleting the view before it goes out of scope is required to make sure all child QML instances
    # are destroyed in the correct order.
    del view
    sys.exit(rc)
