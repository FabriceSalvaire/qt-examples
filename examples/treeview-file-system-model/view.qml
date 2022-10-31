import QtQuick

Item {
    width: 1600
    height: 800

    Component.onCompleted: {
        var index = root_path_index
        console.log('Index row', index.row, index.column)
        // tree_view.expand(index.row)
        // tree_view.expandToIndex(index)
        tree_view.expandRecursively(index.row, -1)
    }

    // https://doc-snapshots.qt.io/qt6-dev/qml-qtquick-treeview.html
    TreeView {
        id: tree_view
        anchors.fill: parent
        anchors.margins: 20
        model: file_system_model

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
                        "Clicked on (row, column):", row, column,
                        "Flags:", "isTreeNode", isTreeNode, "expanded", expanded, "hasChildren", hasChildren, "depth", depth,
                        "Path:", model.filePath,
                        "permission:", model.filePermissions,
                        "icon:", fileIcon
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
                // yield 4 columns: name / size / Mime type / modified date
                //   undocumented
                text: model.display
            }
        }
    }
}
