/*
 * 名称：
 * 说明：
 * 版本：1.0.0
 * 功能：
 * 记录：
 * 1.0.0 -> :
 *      SHA256: E03EA77A209526CF445D74112A4A247B34588AF1DE9DC14C0CE4C586821C25C7
 */
import QtQuick
import FluentUI 1.0

Rectangle {
    id: background
    anchors.fill: parent
    color: "lightblue"

    FluInfoBar{
        id:info_bar
        root: background
    }

    QtObject {
        id: dt
        property int margin: 10
    }

    function showSuccess(text,duration,moremsg){
        return info_bar.showSuccess(text,duration,moremsg)
    }
    function showInfo(text,duration,moremsg){
        return info_bar.showInfo(text,duration,moremsg)
    }
    function showWarning(text,duration,moremsg){
        return info_bar.showWarning(text,duration,moremsg)
    }
    function showError(text,duration,moremsg){
        return info_bar.showError(text,duration,moremsg)
    }
}