# Forked from PySide6/widgets/itemviews/editabletreemodel
# Copyright (C) 2022 The Qt Company Ltd.
# SPDX-License-Identifier: LicenseRef-Qt-Commercial OR BSD-3-Clause
# Copyright (C) 2022 Fabrice Salvaire

####################################################################################################

from pathlib import Path
from typing import Optional, Any
import sys

from PySide6.QtCore import QObject, QAbstractItemModel, QModelIndex, Qt, QUrl, Property, Slot
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
        self._data = data
        self._parent = parent
        self._childs = []

    ##############################################

    @property
    def number_of_columns(self) -> int:
        return len(self._data)

    def data(self, column: int) -> Any:   # QVariant
        if column < 0 or column >= len(self._data):
            return None
        return self._data[column]

    ##############################################

    def set_data(self, column: int, value) -> bool:
        if 0 <= column < len(self._data):
            self._data[column] = value
            return True
        return False

    ##############################################

    def insert_columns(self, position: int, number_of_columns: int) -> bool:
        if position < 0 or position > len(self._data):
            return False
        for column in range(number_of_columns):
            self._data.insert(position, None)
        for child in self._childs:
            child.insert_columns(position, number_of_columns)
        return True

    ##############################################

    def remove_columns(self, position: int, number_of_columns: int) -> bool:
        if position < 0 or position + number_of_columns > len(self._data):
            return False
        for column in range(number_of_columns):
            self._data.pop(position)
        for child in self._childs:
            child.remove_columns(position, number_of_columns)
        return True

    ##############################################

    @property
    def parent(self) -> 'TreeItem':
        return self._parent

    ##############################################

    @property
    def number_of_childs(self) -> int:
        return len(self._childs)

    def child(self, row: int) -> 'TreeItem':
        if 0 <= row < len(self._childs):
            return self._childs[row]
        return None

    @property
    def last_child(self) -> 'TreeItem':
        return self._childs[-1] if self._childs else None

    @property
    def child_index(self) -> int:
        if self._parent:
            return self._parent._childs.index(self)
        return 0

    ##############################################

    def insert_child(self, position: int, number_of_columns: int, count: int = 1) -> bool:
        if 0 <= position <= len(self._childs):
            for row in range(count):
                data = [None] * number_of_columns
                item = TreeItem(data, self)
                self._childs.insert(position, item)
            return True
        return False

    ##############################################

    def remove_child(self, position: int, count: int) -> bool:
        if position < 0 or position + count > len(self._childs):
            return False
        for row in range(count):
            self._childs.pop(position)
        return True

    ##############################################

    def __repr__(self) -> str:
        result = f'<treeitem.TreeItem at 0x{id(self):x}'
        for d in self._data:
            result += f" '{d}'" if d else ' <None>'
        result += f', {len(self._childs)} children>'
        return result

    ##############################################

    # def row(self) -> int:
    #     if self._parent:
    #         return m_parentItem->m_childItems.indexOf(const_cast<TreeItem*>(this))
    #     return 0

####################################################################################################

class TreeModel(QAbstractItemModel):

    # https://doc.qt.io/qt-6/qabstractitemmodel.html

    ##############################################

    def __init__(self, headers: list, data: str, parent: Optional[QObject] = None) -> None:
        super().__init__(parent)
        self._root_data = headers   # Fixem: root_data is unused
        self._root_item = TreeItem(self._root_data.copy())
        self._setup_model_data(data, self._root_item)

    ##############################################

    def _get_item(self, index: QModelIndex = QModelIndex()) -> TreeItem:
        # Return index -> item else root item
        if index.isValid():
            item: TreeItem = index.internalPointer()
            if item:
                return item
        # else
        return self._root_item

    ##############################################

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        '''Returns the number of rows under the given parent.  When the parent is valid it means that
        rowCount is returning the number of children of parent.

        '''
        # https://doc.qt.io/qt-6/qabstractitemmodel.html#rowCount
        # childs are on column = 0
        if parent.isValid() and parent.column() > 0:
            return 0

        parent_item: TreeItem = self._get_item(parent)
        if not parent_item:
            return 0
        return parent_item.number_of_childs

    ##############################################

    def columnCount(self, parent: QModelIndex = None) -> int:
        # if parent.isValid():
        #     return parent.internalPointer().number_of_columns
        return self._root_item.number_of_columns

    ##############################################

    def headerData(
            self,
            section: int,
            orientation: Qt.Orientation,
            role: int = Qt.DisplayRole,
    ) -> Any:   # QVariant
        # root item holds header data
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._root_item.data(section)
        return None

    ##############################################

    def data(self, index: QModelIndex, role: Optional[int] = None) -> Any:   # QVariant
        if not index.isValid():
            return None
        if role not in (Qt.DisplayRole, Qt.EditRole):
            return None
        item: TreeItem = self._get_item(index)
        return item.data(index.column())

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

    def flags(self, index: QModelIndex) -> Qt.ItemFlags:
        # https://doc.qt.io/qt-6/qabstractitemmodel.html#flags
        if not index.isValid():
            return Qt.NoItemFlags
        return Qt.ItemIsEditable | QAbstractItemModel.flags(self, index)

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

    def parent(self, index: QModelIndex = QModelIndex()) -> QModelIndex:
        # https://doc.qt.io/qt-6/qabstractitemmodel.html#parent
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
        success: bool = parent_item.insert_child(position, number_of_columns, rows)
        self.endInsertRows()

        return success

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
        success: bool = parent_item.remove_child(position, rows)
        self.endRemoveRows()
        return success

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
                parent.insert_child(
                    position=parent.number_of_childs,
                    number_of_columns=self._root_item.number_of_columns,
                )
                for i, value in enumerate(column_data):
                    child = parent.last_child
                    child.set_data(i, value)

    ##############################################

    def _repr_recursion(self, item: TreeItem, indent: int = 0) -> str:
        result = ' ' * indent + repr(item) + '\n'
        for child in item._childs:
            result += self._repr_recursion(child, indent + 2)
        return result

    ##############################################

    def __repr__(self) -> str:
        return self._repr_recursion(self._root_item)

####################################################################################################

class QmlApplication(QObject):

    ##############################################

    def __init__(self) -> None:
        super().__init__()
        path = Path(__file__).parent / 'default.txt'
        headers = ['Title', 'Description']
        # tree is encoded in title indentation
        self._model = TreeModel(headers, path.read_text())
        print(self._model)

    ##############################################

    @Property(QObject, constant=True)
    def model(self) -> QObject:
        return self._model

    ##############################################

    # @Slot()
    # def insert_child(self) -> None:
    #     index: QModelIndex = 
    #     if model.columnCount(index) == 0:
    #         if not model.insertColumn(0, index):
    #             return
    #     if not model.insertRow(0, index):
    #         return
    #     for column in range(model.columnCount(index)):
    #         child: QModelIndex = model.index(0, column, index)
    #         model.setData(child, "[No data]", Qt.EditRole)
    #         if not model.headerData(column, Qt.Horizontal):
    #             model.setHeaderData(column, Qt.Horizontal, "[No header]",
    #                                 Qt.EditRole)
    #     selection_model.setCurrentIndex(
    #         model.index(0, 0, index), QItemSelectionModel.ClearAndSelect
    #     )
    #     self.update_actions()

    ##############################################

    # @Slot()
    # def insert_column(self) -> None:
    #     changed: bool = model.insertColumn(column + 1)
    #     if changed:
    #         model.setHeaderData(column + 1, Qt.Horizontal, "[No header]",
    #                             Qt.EditRole)
    #     self.update_actions()

    ##############################################

    # @Slot()
    # def insert_row(self) -> None:
    #     index: QModelIndex = 
    #     parent: QModelIndex = index.parent()
    #     if not model.insertRow(index.row() + 1, parent):
    #         return
    #     self.update_actions()
    #     for column in range(model.columnCount(parent)):
    #         child: QModelIndex = model.index(index.row() + 1, column, parent)
    #         model.setData(child, "[No data]", Qt.EditRole)

    ##############################################

    # @Slot()
    # def remove_column(self) -> None:
    #     if model.removeColumn(column):
    #         self.update_actions()

    ##############################################

    # @Slot()
    # def remove_row(self) -> None:
    #     index: QModelIndex = 
    #     if model.removeRow(index.row(), index.parent()):
    #         self.update_actions()

####################################################################################################

if __name__ == '__main__':
    app = QGuiApplication(sys.argv)
    view = QQuickView()
    context = view.rootContext()
    view.setResizeMode(QQuickView.SizeRootObjectToView)

    qml_appplication = QmlApplication()
    context.setContextProperty('application', qml_appplication)

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
