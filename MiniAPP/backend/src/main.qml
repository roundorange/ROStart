import QtQuick
import QtQuick.Layouts
import QtQuick.Controls
import QtQuick.Window

Rectangle {
    anchors.fill: parent
    color: "#00A0D6"

    ColumnLayout{
        anchors.fill: parent
        anchors.margins: 20

        Item{Layout.fillHeight: true; Layout.fillWidth: true}

        Rectangle {
            id: states
            Layout.alignment: Qt.AlignCenter
            height: 50
            width: 160
            radius: 15
            Text {
                anchors.centerIn: parent
                font.pixelSize: 20;
                text: "后端模板小程序"
            }
        }

        Item{Layout.fillHeight: true; Layout.fillWidth: true}
        Item{Layout.fillHeight: true; Layout.fillWidth: true}

        Button {
            text: '测试按钮'

            Layout.alignment: Qt.AlignCenter
            hoverEnabled: false

            background: Rectangle {
                implicitWidth: 100
                implicitHeight: 40
                color: parent.down ? Qt.darker("#ffffff") : "#ffffff"
                border.width: 0
                radius: 15
            }
            onClicked: {
                console.log("点击测试按钮")
                backend.debug("msg")
            }
        }
        Button {
            id: btnexit
            text: '退出子程序'

            Layout.alignment: Qt.AlignCenter
            hoverEnabled: false

            background: Rectangle {
                implicitWidth: 100
                implicitHeight: 40
                color: parent.down ? Qt.darker("#ffffff") : "#ffffff"
                border.width: 0
                radius: 15
            }
            onClicked: {
                console.log("点击退出按钮")
                backend.quitAPP()  // 退出子程序
            }
        }
        Item{Layout.fillHeight: true; Layout.fillWidth: true}
    }
}