// Copyright (C) 2022 Fabrice Salvaire
// SPDX-License-Identifier: BSD-3-Clause

import QtQuick

Item {
    width: 1600
    height: 800

    Component.onCompleted: {
        tree_view.expandRecursively()
    }

    // https://doc-snapshots.qt.io/qt6-dev/qml-qtquick-treeview.html
    TreeView {
        id: tree_view
        anchors.fill: parent
        anchors.margins: 20
        model: application.model

        delegate: Item {
            id: tree_delegate

            implicitWidth: padding + label.x + label.implicitWidth + padding
            implicitHeight: label.implicitHeight * 1.5

            readonly property real indent: 20
            readonly property real padding: 5

            // Assigned by TreeView:
            required property TreeView treeView
            required property bool isTreeNode
            required property bool expanded
            required property int hasChildren
            required property int depth

            TapHandler {
                onTapped: {
                    treeView.toggleExpanded(row)
                    console.log(
                        "Clicked on (row, column):", row, column
                    )
                }
            }

            HoverHandler {
                id: hover_handler
            }

            Text {
                id: indicator
                visible: tree_delegate.isTreeNode && tree_delegate.hasChildren
                x: padding + tree_delegate.depth * tree_delegate.indent
                anchors.verticalCenter: label.verticalCenter
                text: "▸"
                rotation: tree_delegate.expanded ? 90 : 0
            }

            Text {
                id: label
                x: padding + (tree_delegate.isTreeNode ? (tree_delegate.depth + 1) * tree_delegate.indent : 0)
                width: tree_delegate.width - tree_delegate.padding - x
                clip: true
                color: hover_handler.hovered ? "red" : "black"
                text: model.display
            }
        }
    }
}
