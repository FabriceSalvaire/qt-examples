import QtQuick

Rectangle {
    id: window
    width: 320
    height: 480
    // focus: true

    Component.onCompleted: {
        console.info("Touch Application")
    }

    Rectangle {
        anchors.fill: parent
        color: "steelblue"
        focus: true // required for key event

        // https://doc.qt.io/qt-6/qml-qtquick-keys.html
        Keys.onPressed: (event) => {
            console.info("Key pressed", event.key);
            if (event.key == Qt.Key_Left) {
                console.info("move left");
                event.accepted = true;
            }
        }
        // Keys.onLeftPressed: console.info("move left")

        MouseArea {
            enabled: false
            anchors.fill: parent
            onPressed: (event) => {
                console.info("onPressed", mouseX, " ", mouseY)
            }
            onPositionChanged: (event) => {
                console.info("onPositionChanged", mouseX, " ", mouseY)
            }
            onReleased: (event) => {
                console.info("onReleased", mouseX, " ", mouseY)
            }
            // canceled()
            // clicked(MouseEvent mouse)
            // doubleClicked(MouseEvent mouse)
            // entered()
            // exited()
            // positionChanged(MouseEvent mouse)
            // pressAndHold(MouseEvent mouse)
            // pressed(MouseEvent mouse)
            // released(MouseEvent mouse)
            // wheel(WheelEvent wheel)
        }

        // https://doc.qt.io/qt-6/qml-qtquick-wheelhandler.html
        WheelHandler {
            enabled: false
            // The property to be modified on the target when the mouse wheel is rotated.
            property: "rotation"
            onWheel: (event)=> console.info(
                "rotation", event.angleDelta.y,
                "scaled", rotation, "@", point.position,
                "=>", parent.rotation
            )
        }

        // https://doc.qt.io/qt-6/qml-qtquick-pointhandler.html
        // PointHandler {
        // }

        // https://doc.qt.io/qt-6/qml-qtquick-taphandler.html
        TapHandler {
            enabled: false // grabed by MultiPointHandler
            id: tap_handler

            // Mouse TouchScreen TouchPad Stylus Keyboard
            acceptedDevices: PointerDevice.AllDevices

            // GenericPointer Finger Pen
            acceptedPointerTypes: PointerDevice.AllPointerTypes

            // acceptedButtons: Qt.RightButton
            // acceptedModifiers :

            // At the time of release (the mouse button is released or the finger is lifted),
            // if the event point is outside the bounds of the parent Item, a tap gesture is not recognized.
            gesturePolicy: TapHandler.ReleaseWithinBounds

            // dragThreshold
            // :grabPermissions:
            // longPressThreshold:
            // margin:

            onTapped: (event_point, button) => console.info(
                "tapped", event_point.device.name,
                "button", button,
                "@", event_point.scenePosition
            )

            onSingleTapped: (event_point, button) => console.info(
                "single tapped", event_point.device.name,
                "button", button,
                "@", event_point.scenePosition
            )

            onDoubleTapped: (event_point, button) => console.info(
                "double tapped", event_point.device.name,
                "button", button,
                "@", event_point.scenePosition
            )
        }

        // https://doc.qt.io/qt-6/qml-qtquick-pinchhandler.html
        // PinchHandler is a handler that interprets a multi-finger gesture to interactively rotate, zoom, and drag an Item.
        // Like other Input Handlers, by default it is fully functional, and manipulates its target, which is the Item within which it is declared.
        PinchHandler {
            enabled: false // not grabed by MultiPointHandler
            id: handler
            target: null
            onScaleChanged: console.info("onScaleChange", handler.scale)
        }

        // https://doc.qt.io/qt-6/qml-qtquick-pincharea.html
        PinchArea {
            enabled: false
            onPinchStarted: (pinch) => console.info("onPinchStarted")
            onPinchUpdated: (pinch) => console.info("onPinchUpdated")
            onPinchFinished: (pinch) => console.info("onPinchFinished")
            onSmartZoom: (pinch) => console.info("onSmartZoom")
        }

        // https://doc.qt.io/qt-6/qml-qtquick-multipointtoucharea.html
        MultiPointTouchArea {
            id: multi_point_touch_area
            enabled: true
            anchors.fill: parent
            touchPoints: [
                TouchPoint { id: point1 },
                TouchPoint { id: point2 }
            ]
            function format_point(point) {
                return "Point1 " + point.x.toFixed(1) + ", " + point.y.toFixed(1)
            }
            function format_points(point) {
                return format_point(point1) + " " + format_point(point2)
            }
            onCanceled: (gesture) => {
                console.info("onCanceled", format_points())
            }
            onGestureStarted: (gesture) => {
                console.info("onGestureStarted", format_points())
            }
            onPressed: (gesture) => {
                console.info("onPressedStarted", format_points())
            }
            onReleased: (gesture) => {
                console.info("onReleasedStarted", format_points())
            }
            onTouchUpdated: (gesture) => {
                console.info("onTouchUpdated", format_points())
            }
            // onUpdated: (gesture) => {
            //     console.info("onUpdated", format_points())
            // }
        }

        // https://doc.qt.io/qt-6/qml-qtquick-flickable.html
        // Flickable {
        //     enabled: true
        //     anchors.fill: parent
        //     boundsBehavior: Flickable.DragAndOvershootBounds 
        //     contentWidth: 1000000
        //     contentHeight: 1000000
        //
        //     Item {}
        //
        //     onFlickStarted: console.info("onFlickStarted")
        //     onFlickEnded: console.info("onFlickEnded")
        //     onMovementStarted: console.info("onMovementStarted ", horizontalVelocity, verticalVelocity)
        //     onMovementEnded: console.info("onMovementEnded")
        // }

        Column {
            Text {
                color: handler.active ? "darkgreen" : "black"
                text: handler.rotation.toFixed(1) + " degrees\n" +
                    handler.translation.x.toFixed(1) + ", " + handler.translation.y.toFixed(1) + "\n" +
                    (handler.scale * 100).toFixed(1) + "%"
            }

            Text {
                text: multi_point_touch_area.format_point(point1)
            }

            Text {
                text: multi_point_touch_area.format_point(point2)
            }
        }
    }
}
