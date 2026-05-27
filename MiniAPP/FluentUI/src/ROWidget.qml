import QtQuick
import QtQuick.Layouts
import QtQuick.Controls
import QtQuick.Window
import FluentUI

Rectangle {
    id: background
    anchors.fill: parent
    color: "#00A0D6"

    FluInfoBar {
        id: info_bar
        root: background
    }
}