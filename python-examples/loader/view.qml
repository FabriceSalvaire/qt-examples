// Copyright (C) 2022 Fabrice Salvaire
// SPDX-License-Identifier: BSD-3-Clause

import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Item {
    width: 1000
    height: 800

    Component {
        id: component1

        Rectangle {
            color: "#AA0000"
      }
    }

    RowLayout {
        spacing: 10

        ColumnLayout {
            id: buttons
            width: parent.width * .25
            height: parent.height
            Layout.margins: 10

            Button {
                text: 'load1'
                onClicked: placeholder1.sourceComponent = component1
            }

            Button {
                text: 'load2'
                onClicked: placeholder2.source = 'MyItem.qml'
            }

            Button {
                text: 'load2'
                onClicked: {
                }
            }
        }

        ColumnLayout {
            width: parent.width - buttons.width
            height: parent.height
            Layout.margins: 10

            Item {
                width: 200
                height: 200

                Rectangle {
                    visible: placeholder1.status !== Loader.Ready
                    anchors.fill: parent
                    border.color: "black"
                    border.width: 2

                    Text {
                        anchors.centerIn: parent
                        text: 'placeholder1'
                    }
                }

                Loader {
                    id: placeholder1
                    anchors.fill: parent
                    // active: true
                    // asynchronous: false

                    onStatusChanged: {
                        if (status == Loader.Ready)
                            console.log('Placeholder1 loaded')
                    }
                }
            }

            Item {
                width: 200
                height: 200

                Rectangle {
                    visible: placeholder2.status !== Loader.Ready
                    anchors.fill: parent
                    border.color: "black"
                    border.width: 2

                    Text {
                        anchors.centerIn: parent
                        text: 'placeholder2'
                    }
                }

                Loader {
                    id: placeholder2
                    anchors.fill: parent

                    onStatusChanged: {
                        if (status == Loader.Ready)
                            console.log('Placeholder2 loaded')
                    }
                }

                Connections {
                    target: placeholder2.item
                    function onMessage(msg) { console.log(msg) }
                }

                Binding {
                    target: placeholder2.item
                    property: "integer"
                    value: 123
                }
            }
        }
    }
}
