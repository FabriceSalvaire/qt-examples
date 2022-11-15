// Copyright (C) 2022 Fabrice Salvaire
// SPDX-License-Identifier: BSD-3-Clause

import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Item {
    width: 1000
    height: 600

    Rectangle {
	id: pinch_target
	width: 50
	height: width
        radius: width / 2
	color: "red"
    }

    // https://doc.qt.io/qt-6/qml-qtquick-mousearea.html
    /* MouseArea { */
    /*     anchors.fill: parent */

    /*     acceptedButtons: Qt.AllButtons */
    /*     cursorShape: Qt.ArrowCursor */

    /*     // Handle also tap */
    /*     onClicked: (mouse) => { */
    /*         console.log("MouseArea clicked", mouse.x, mouse.y, mouse.button, mouse.modifiers) */
    /*     } */
    /*     onDoubleClicked: (mouse) => { */
    /*         console.log("MouseArea double clicked", mouse.x, mouse.y, mouse.button, mouse.modifiers) */
    /*     } */

    /*     // https://doc.qt.io/qt-6/qml-qtquick-wheelevent.html */
    /*     // Handle also the corresponding tablet gesture */
    /*     onWheel: (wheel) => { */
    /*         console.log("MouseArea wheel", wheel.angleDelta) */
    /*     } */
    /*     // WheelHandler */
    /*     // https://doc.qt.io/qt-6/qml-qtquick-wheelhandler.html */

    /*     // onCanceled() */
    /*     // onEntered() */
    /*     // onExited() */
    /*     // onPositionChanged */
    /*     // onPressAndHold */
    /*     // onPressed */
    /*     // onReleased */
    /* } // MouseArea */

    // https://doc.qt.io/qt-6/qml-qtquick-pinchhandler.html
    PinchHandler {
	target: pinch_target
    }
}
