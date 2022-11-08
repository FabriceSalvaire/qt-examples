// Copyright (C) 2022 Fabrice Salvaire
// SPDX-License-Identifier: BSD-3-Clause

import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Item {
    width: 1600
    height: 800

    GridLayout {
        id: grid
        anchors.fill: parent
        columns: 3
        rows: 2

        // MouseArea
        Rectangle {
            width: grid.width / 3
            height: grid.height / 2
            border.width: 2

            Text {
                anchors.centerIn: parent
                text: "MouseArea"
            }

            // https://doc.qt.io/qt-6/qml-qtquick-mousearea.html
            // Wacom: tap
            MouseArea {
                anchors.fill: parent

                // mouseX
                // mouseY
                // containsMouse: bool
                // containsPress: bool
                // pressed
                // pressedButtons

                // enabled:
                // hoverEnabled:

                acceptedButtons: Qt.AllButtons
                cursorShape: Qt.ArrowCursor
                // pressAndHoldInterval:
                // preventStealing:
                // propagateComposedEvents:
                // scrollGestureEnabled:

                // drag.active: bool
                // drag.axis: enumeration
                // drag.filterChildren: bool
                // drag.maximumX: real
                // drag.maximumY: real
                // drag.minimumX: real
                // drag.minimumY: real
                // drag.smoothed: bool
                // drag.target: Item
                // drag.threshold: real

                // https://doc.qt.io/qt-6/qml-qtquick-mouseevent.html

                onClicked: (mouse) => {
                    console.log("MouseArea clicked", mouse.x, mouse.y, mouse.button, mouse.modifiers)
                }
                // onDoubleClicked

                // https://doc.qt.io/qt-6/qml-qtquick-wheelevent.html
                onWheel: (wheel) => {
                    console.log("MouseArea wheel", wheel.angleDelta)
                }
                // WheelHandler
                // https://doc.qt.io/qt-6/qml-qtquick-wheelhandler.html

                // onCanceled()
                // onEntered()
                // onExited()
                // onPositionChanged
                // onPressAndHold
                // onPressed
                // onReleased
            }
        } // MouseArea

        // MultiPointTouchArea
        Rectangle {
            width: grid.width / 3
            height: grid.height / 2
            border.width: 2

            Text {
                anchors.centerIn: parent
                text: "MultiPointTouchArea"
            }

            // https://doc.qt.io/qt-6/qml-qtquick-multipointtoucharea.html
            // Wacom:
            //    drag with double-tap & move
            MultiPointTouchArea {
                anchors.fill: parent

                mouseEnabled: true
                minimumTouchPoints: 1
                maximumTouchPoints: 2

                touchPoints: [
                    TouchPoint { id: point1 },
                    TouchPoint { id: point2 }
                ]

                Rectangle {
                    width: 30
                    height: width
                    color: "green"
                    x: point1.x
                    y: point1.y
                }

                Rectangle {
                    width: 30
                    height: width
                    color: "blue"
                    x: point2.x
                    y: point2.y
                }

                // https://doc.qt.io/qt-6/qml-qtquick-touchpoint.html

                onTouchUpdated: (points) => {
                    for (var i = 0; i < points.length; i++) {
                        var point = points[i]
                        console.log("MultiPointTouchArea", point.pointId, point.x, point.y)
                    }
                }

                // https://doc.qt.io/qt-6/qml-qtquick-gestureevent.html
                onGestureStarted: (gesture) => {
                    console.log("MultiPointTouchArea gesture started")
                }

                // canceled(list<TouchPoint> touchPoints)
                // pressed(list<TouchPoint> touchPoints)
                // released(list<TouchPoint> touchPoints)
                // updated(list<TouchPoint> touchPoints)
            }
        } // MultiPointTouchArea

        // PinchArea
        Rectangle {
            width: grid.width / 3
            height: grid.height / 2
            border.width: 2

            Text {
                anchors.centerIn: parent
                text: "PinchArea"
            }

            // https://doc.qt.io/qt-6/qml-qtquick-pincharea.html
            // Wacom:
            //    ???
            PinchArea {
                // pinch.active : bool
                // pinch.dragAxis : enumeration
                // pinch.maximumRotation : real
                // pinch.maximumScale : real
                // pinch.maximumX : real
                // pinch.maximumY : real
                // pinch.minimumRotation : real
                // pinch.minimumScale : real
                // pinch.minimumX : real
                // pinch.minimumY : real
                // pinch.target : Item

                // pinchFinished(PinchEvent pinch)
                // pinchStarted(PinchEvent pinch)
                // pinchUpdated(PinchEvent pinch)
                // smartZoom(PinchEvent pinch)
            }

            // PinchHandler
            // https://doc.qt.io/qt-6/qml-qtquick-pinchhandler.html
        } // PinchArea

        // PointHandler
        Rectangle {
            id: point_handler_scope
            width: grid.width / 3
            height: grid.height / 2
            border.width: 2

            Text {
                anchors.centerIn: parent
                text: "PointHandler"
            }

            // https://doc.qt.io/qt-6/qml-qtquick-pointhandler.html
            // Wacom:
            //    reacts to tap
            //    drag with double-tap & move
            PointHandler {
                // Handler for reacting to a single touchpoint
                id: handler

                acceptedDevices: PointerDevice.AllDevices
                acceptedButtons: Qt.AllButtons
                // acceptedModifiers:

                // acceptedPointerTypes: flags
                // active: bool
                // cursorShape: Qt::CursorShape
                // dragThreshold: int
                // grabPermissions: flags
                // margin: real
                // parent:
                // point: HandlerPoint

                // canceled(EventPoint point)
                // grabChanged(GrabTransition transition, EventPoint point)

                target: Rectangle {
                    parent: point_handler_scope
                    width: 20
                    height: width
                    radius: width / 2
                    color: "red"
                    visible: handler.active
                    x: handler.point.position.x - width / 2
                    y: handler.point.position.y - height / 2
                }
            }
        } // PointHandler

        // Taphandler
        Rectangle {
            id: button
            width: grid.width / 3
            height: grid.height / 2
            border.width: 2

            signal clicked

            property color dark: Qt.darker(palette.button, 1.3)
            gradient: Gradient {
                GradientStop { position: 0.0; color: tap_handler.pressed ? button.dark : palette.button }
                GradientStop { position: 1.0; color: button.dark }
            }

            Text {
                anchors.centerIn: parent
                text: "TapHandler"
            }

            // https://doc.qt.io/qt-6/qml-qtquick-taphandler.html
            // Wacom: tap
            TapHandler {
                id: tap_handler
                gesturePolicy: TapHandler.ReleaseWithinBounds
                onTapped: button.clicked()
            }
        } // TapHandler
    }
}
