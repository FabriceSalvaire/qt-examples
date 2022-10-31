// Forked from Qt source
// Copyright (C) 2022 The Qt Company Ltd.
// SPDX-License-Identifier: LicenseRef-Qt-Commercial OR BSD-3-Clause
// Copyright (C) 2022 Fabrice Salvaire

// from Fusion style

import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import QtQuick.Templates as T
// import QtQuick.Controls.impl
// import QtQuick.Controls.Fusion
// import QtQuick.Controls.Fusion.impl

Page {
    id: root
    width: 1800
    height: 800

    property int number_of_items: 50
    property int item_height: 30 // was 21

    // To place in VerticalTabBar.qml
    TabBar {
        id: control
        width: 200

        // ! first/last item can be half clipped for some item height ???
        height: parent.height // - 10
        anchors.verticalCenter: parent.verticalCenter

        // https://doc.qt.io/qt-6/qml-qtquick-listview.html
        contentItem: ListView {
            model: control.contentModel
            currentIndex: control.currentIndex

            spacing: control.spacing
            orientation: ListView.Vertical
            // the contents can not be dragged beyond the boundary of the flickable, and flicks will not overshoot
            boundsBehavior: Flickable.StopAtBounds
            // allows flicking vertically if the contentHeight is greater than the height of the Flickable
            flickableDirection: Flickable.AutoFlickIfNeeded
            snapMode: ListView.SnapToItem

            highlightMoveDuration: 0
            highlightRangeMode: ListView.ApplyRange
            preferredHighlightBegin: 40
            preferredHighlightEnd: width - 40
        }

        Repeater {
            model: number_of_items

            // To place in VerticalTabButton.qml
            TabButton {
                id: control2
                width: control.width // ! else width is divided by the number of items, due to hardcoded horizontal behaviour
                text: "tab blabla blabla %1".arg(model.index + 1)

                contentItem: IconLabel {
                    spacing: control2.spacing
                    mirrored: control2.mirrored
                    display: control2.display

                    icon: control2.icon
                    text: control2.text
                    font: control2.font
                    color: control2.palette.buttonText
                }

                background: Rectangle {
                    y: control2.checked || control2.TabBar.position !== T.TabBar.Header ? 0 : 2
                    implicitHeight: item_height
                    height: control2.height - (control2.checked ? 0 : 2)

                    border.color: Qt.lighter(Fusion.outline(control2.palette), 1.1)
                    border.width: 0

                    gradient: Gradient {
                        GradientStop {
                            position: 0
                            color: control2.checked ? Qt.lighter(Fusion.tabFrameColor(control2.palette), 1.04)
                                : Qt.darker(Fusion.tabFrameColor(control2.palette), 1.08)
                        }
                        GradientStop {
                            position: control2.checked ? 0 : 0.85
                            color: control2.checked ? Qt.lighter(Fusion.tabFrameColor(control2.palette), 1.04)
                                : Qt.darker(Fusion.tabFrameColor(control2.palette), 1.08)
                        }
                        GradientStop {
                            position: 1
                            color: control2.checked ? Fusion.tabFrameColor(control2.palette)
                                : Qt.darker(Fusion.tabFrameColor(control2.palette), 1.16)
                        }
                    }
                }
            }
        }
    }

    StackLayout {
        id: stack_layout
        width: parent.width - control.width
        height: parent.height

        currentIndex: control.currentIndex

        Repeater {
            model: number_of_items
            Item {
                Label {
                    anchors.centerIn: parent
                    text: "tab %1".arg(model.index + 1)
                    font.pixelSize: 50
                }
            }
        }
    }
}
