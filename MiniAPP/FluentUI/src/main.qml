import QtQuick
import QtQuick.Layouts
import QtQuick.Controls
import QtQuick.Window
import FluentUI

ROWidget {
    id: background
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
            FluCopyableText {
                anchors.centerIn: parent
                font.pixelSize: 20;
                text: "FluentUI小程序"
            }
        }

        Item{Layout.fillHeight: true; Layout.fillWidth: true}
        Item{Layout.fillHeight: true; Layout.fillWidth: true}

        FluTextBox{
            Layout.fillWidth: true
            Layout.preferredWidth: 2
            font.pixelSize: 16
            placeholderText: qsTr("代码路径")
            text: "单行输入框"
        }

        FluButton {
            id: btn
            text: "测试按钮"
            Layout.alignment: Qt.AlignCenter
            implicitWidth: 120
            implicitHeight: 40
            onClicked: {
                console.log("点击测试按钮")
                info_bar.showSuccess("激活成功",1000,"请重启应用")
            }
        }

        FluButton {
            id: btnexit
            text: "退出子程序"
            Layout.alignment: Qt.AlignCenter
            implicitWidth: 120
            implicitHeight: 40
            onClicked: {
                console.log("点击退出按钮")
                Qt.quit()  // 退出子程序
            }
        }
        Item{Layout.fillHeight: true; Layout.fillWidth: true}
    }
    FluInfoBar {
        id: info_bar
        root: background
    }
}