# Forked from PySide6/widgets/itemviews/editabletreemodel
# Copyright (C) 2022 The Qt Company Ltd.
# SPDX-License-Identifier: LicenseRef-Qt-Commercial OR BSD-3-Clause
# Copyright (C) 2022 Fabrice Salvaire

####################################################################################################

from pathlib import Path
from typing import Optional, Any
import sys

from PySide6.QtCore import QObject, QAbstractItemModel, QModelIndex, Qt, QUrl
from PySide6.QtGui import QGuiApplication
from PySide6.QtQuick import QQuickView
from PySide6.QtQml import QQmlContext

####################################################################################################

import os
os.environ['QT_LOGGING_RULES'] = ';'.join((
    '*.debug=true',
    'qt.*.debug=false',
    '*.info=true',
))

####################################################################################################

class TreeItem:

    ##############################################

    def __init__(self, data: list, parent: Optional['TreeItem'] = None) -> None:
        self._item_data = data
        self._parent_item = parent
        self._child_items = []

    ##############################################

    # parent_item
    @property
    def parent(self):
        return self._parent_item

    ##############################################

    # append_child
    def insert_children(self, position: int, number_of_columns: int, count: int = 1) -> bool:
        if 0 <= position <= len(self._child_items):
            for row in range(count):
                data = [None] * number_of_columns
                item = TreeItem(data, self)
                self._child_items.insert(position, item)
            return True
        return False

    ##############################################

    def child(self, row: int) -> 'TreeItem':
        if 0 <= row < len(self._child_items):
            return self._child_items[row]
        return None

    ##############################################

    @property
    def number_of_childs(self) -> int:
        return len(self._child_items)

    ##############################################

    @property
    def child_index(self) -> int:
        if self._parent_item:
            return self._parent_item._child_items.index(self)
        return 0

    ##############################################

    @property
    def number_of_columns(self) -> int:
        return len(self._item_data)

    ##############################################

    @property
    def last_child(self):
        return self._child_items[-1] if self._child_items else None

    ##############################################

    def data(self, column: int) -> Any:   # QVariant
        if column < 0 or column >= len(self._item_data):
            return None
        return self._item_data[column]

    ##############################################

    def insert_columns(self, position: int, number_of_columns: int) -> bool:
        if position < 0 or position > len(self._item_data):
            return False
        for column in range(number_of_columns):
            self._item_data.insert(position, None)
        for child in self._child_items:
            child.insert_columns(position, number_of_columns)
        return True

    ##############################################

    def remove_children(self, position: int, count: int) -> bool:
        if position < 0 or position + count > len(self._child_items):
            return False
        for row in range(count):
            self._child_items.pop(position)
        return True

    ##############################################

    def remove_columns(self, position: int, number_of_columns: int) -> bool:
        if position < 0 or position + number_of_columns > len(self._item_data):
            return False
        for column in range(number_of_columns):
            self._item_data.pop(position)
        for child in self._child_items:
            child.remove_columns(position, number_of_columns)
        return True

    ##############################################

    def set_data(self, column: int, value) -> bool:
        if 0 <= column < len(self._item_data):
            self._item_data[column] = value
            return True
        return False

    ##############################################

    def __repr__(self) -> str:
        result = f'<treeitem.TreeItem at 0x{id(self):x}'
        for d in self._item_data:
            result += f" '{d}'" if d else ' <None>'
        result += f', {len(self._child_items)} children>'
        return result

    ##############################################

    # def row(self) -> int:
    #     if self._parent_item:
    #         return m_parentItem->m_childItems.indexOf(const_cast<TreeItem*>(this))
    #     return 0

####################################################################################################

class TreeModel(QAbstractItemModel):

    ##############################################

    def __init__(self, headers: list, data: str, parent: Optional[QObject] = None) -> None:
        super().__init__(parent)
        self._root_data = headers   # Fixem: root_data is unused
        self._root_item = TreeItem(self._root_data.copy())
        self._setup_model_data(data, self._root_item)

    ##############################################

    def columnCount(self, parent: QModelIndex = None) -> int:
        # if parent.isValid():
        #     return parent.internalPointer().number_of_columns
        return self._root_item.number_of_columns

    ##############################################

    def data(self, index: QModelIndex, role: Optional[int] = None) -> Any:   # QVariant
        if not index.isValid():
            return None
        if role not in (Qt.DisplayRole, Qt.EditRole):
            return None
        item: TreeItem = self._get_item(index)
        return item.data(index.column())

    ##############################################

    def flags(self, index: QModelIndex) -> Qt.ItemFlags:
        if not index.isValid():
            return Qt.NoItemFlags
        return Qt.ItemIsEditable | QAbstractItemModel.flags(self, index)

    ##############################################

    def _get_item(self, index: QModelIndex = QModelIndex()) -> TreeItem:
        if index.isValid():
            item: TreeItem = index.internalPointer()
            if item:
                return item
        # Fixme: ok ???
        return self._root_item

    ##############################################

    def headerData(
            self,
            section: int,
            orientation: Qt.Orientation,
            role: int = Qt.DisplayRole,
    ) -> Any:   # QVariant
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._root_item.data(section)
        return None

    ##############################################

    def index(
            self,
            row: int,
            column: int,
            parent: QModelIndex = QModelIndex(),
    ) -> QModelIndex:
        # if (!hasIndex(row, column, parent))
        if parent.isValid() and parent.column() != 0:
            return QModelIndex()

        parent_item: TreeItem = self._get_item(parent)
        if not parent_item:
            return QModelIndex()

        child_item: TreeItem = parent_item.child(row)
        if child_item:
            return self.createIndex(row, column, child_item)
        return QModelIndex()

    ##############################################

    def insertColumns(
            self,
            position: int,
            number_of_columns: int,
            parent: QModelIndex = QModelIndex(),
    ) -> bool:
        self.beginInsertColumns(parent, position, position + number_of_columns - 1)
        success: bool = self._root_item.insert_columns(position, number_of_columns)
        self.endInsertColumns()
        return success

    ##############################################

    def insertRows(
            self,
            position: int,
            rows: int,
            parent: QModelIndex = QModelIndex(),
    ) -> bool:
        parent_item: TreeItem = self._get_item(parent)
        if not parent_item:
            return False

        self.beginInsertRows(parent, position, position + rows - 1)
        number_of_columns = self._root_item.number_of_columns
        success: bool = parent_item.insert_children(position, number_of_columns, rows)
        self.endInsertRows()

        return success

    ##############################################

    def parent(self, index: QModelIndex = QModelIndex()) -> QModelIndex:
        if not index.isValid():
            return QModelIndex()

        child_item: TreeItem = self._get_item(index)
        if child_item:
            parent_item: TreeItem = child_item.parent
        else:
            parent_item = None

        if parent_item == self._root_item or not parent_item:
            return QModelIndex()

        return self.createIndex(parent_item.child_index, 0, parent_item)

    ##############################################

    def removeColumns(
            self,
            position: int,
            number_of_columns: int,
            parent: QModelIndex = QModelIndex(),
    ) -> bool:
        self.beginRemoveColumns(parent, position, position + number_of_columns - 1)
        success: bool = self._root_item.remove_columns(position, number_of_columns)
        self.endRemoveColumns()
        if self._root_item.number_of_columns == 0:
            self.removeRows(0, self.rowCount())
        return success

    ##############################################

    def removeRows(
            self,
            position: int,
            rows: int,
            parent: QModelIndex = QModelIndex(),
    ) -> bool:
        parent_item: TreeItem = self._get_item(parent)
        if not parent_item:
            return False
        self.beginRemoveRows(parent, position, position + rows - 1)
        success: bool = parent_item.remove_children(position, rows)
        self.endRemoveRows()
        return success

    ##############################################

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        if parent.isValid() and parent.column() > 0:
            return 0

        parent_item: TreeItem = self._get_item(parent)
        if not parent_item:
            return 0

        return parent_item.number_of_childs

    ##############################################

    def setData(self, index: QModelIndex, value, role: int) -> bool:
        if role != Qt.EditRole:
            return False
        item: TreeItem = self._get_item(index)
        result: bool = item.set_data(index.column(), value)
        if result:
            self.dataChanged.emit(index, index, [Qt.DisplayRole, Qt.EditRole])
        return result

    ##############################################

    def setHeaderData(
            self,
            section: int,
            orientation: Qt.Orientation,
            value,
            role: int = None,
    ) -> bool:
        if role != Qt.EditRole or orientation != Qt.Horizontal:
            return False
        result: bool = self._root_item.set_data(section, value)
        if result:
            self.headerDataChanged.emit(orientation, section, section)
        return result

    ##############################################

    def _setup_model_data(self, data: str, parent: TreeItem) -> None:
        parents = [parent]
        indentations = [0]
        for line in data.split('\n'):
            line = line.rstrip()
            if line and '\t' in line:
                # process line
                position = 0
                while position < len(line):
                    if line[position] != ' ':
                        break
                    position += 1
                _ = line[position:].split('\t')
                column_data = [string for string in _ if string]

                # handle indentation
                if position > indentations[-1]:
                    if parents[-1].number_of_childs > 0:
                        parents.append(parents[-1].last_child)
                        indentations.append(position)
                else:
                    while position < indentations[-1] and parents:
                        parents.pop()
                        indentations.pop()

                # insert data
                parent: TreeItem = parents[-1]
                parent.insert_children(
                    position=parent.number_of_childs,
                    number_of_columns=self._root_item.number_of_columns,
                )
                for i, value in enumerate(column_data):
                    child = parent.last_child
                    child.set_data(i, value)

    ##############################################

    def _repr_recursion(self, item: TreeItem, indent: int = 0) -> str:
        result = ' ' * indent + repr(item) + '\n'
        for child in item._child_items:
            result += self._repr_recursion(child, indent + 2)
        return result

    ##############################################

    def __repr__(self) -> str:
        return self._repr_recursion(self._root_item)

####################################################################################################

class CustomCode:
    def __init__(self, context: QQmlContext) -> None:
        path = Path(__file__).parent / 'default.txt'
        headers = ['Title', 'Description']
        # tree is encoded in title indentation
        self._model = TreeModel(headers, path.read_text())
        print(self._model)
        context.setContextProperty('tree_model', self._model)

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
