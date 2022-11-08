// Copyright (C) 2022 Fabrice Salvaire
// SPDX-License-Identifier: BSD-3-Clause

import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Rectangle {
    id: root

    signal message(string msg)

    property int integer

    Component.onCompleted: {
        console.log("integer", integer)
    }

    color: "#00AA00"

    MouseArea {
        anchors.fill: parent
        onClicked: root.message("clicked %1".arg(integer))
    }
}
