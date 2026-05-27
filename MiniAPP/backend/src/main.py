#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###----------1、文件说明----------###
'''
* 说明：小程序基础模板
* 时间：2025-09-22
* 文件：
* 作者：ROrange
* 版本：
 - 1.0 -> : 小程序基础模板
    SHA256: F943364A1E67407DB7A7118CA551BDC56923EAD38C798B4BD7D1EE36694BB776
 - 1.1 -> : 修改qml出错时，不能正常显示的问题。
            与 appcode-v2.2.py 配合使用
    SHA256: 58657BF84CE6FEB7EFD32F7FC64F524F25385D7C74302EB05364D919015B5F86
 - 1.2 -> 2026-03-20 ：支持应用程序显示logo
    SHA256: E6BBA04E30A78B69FEC6C456E2ED379C168E33C14C34C2D5DE770B0AB6F03064
 - 1.3 -> 2026-05-23 : 支持显示配置文件中的标题、logo
    SHA256: 50B7C4BC62F17BC8D3A5C52DD5D83E8197CB98EB90D09D4209B7115B91C0DE3E
* 备注：
'''
###----------2、库导入----------###
import os, sys
import json
import uuid, json
import http.client
from loguru import logger as log
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from PySide6.QtCore import QUrl
from PySide6.QtQuick import QQuickWindow
from PySide6.QtQml import QQmlEngine, QQmlComponent
from PySide6.QtCore import qInstallMessageHandler, QtMsgType, qWarning
from PySide6.QtQuickControls2 import QQuickStyle

from appcode import mainWindow

###----------3、参数配置----------###
# 调试日志输出端口
logsip = '192.168.10.20:54444'


###----------4、功能程序----------###
def post_to_remote(message):
    """将日志通过POST发送到远程服务器"""
    log_entry = {
        "file": message.record["file"].name,
        "filepath": message.record["file"].path,
        "function": message.record["function"],
        "level": message.record["level"].name,
        "line": message.record["line"],
        "module": message.record["module"],
        "message": message.record["message"],
        "process": message.record["process"].name + "(" + str(message.record["process"].id) + ")",
        "thread": message.record["thread"].name + "(" + str(message.record["thread"].id) + ")",
        "timestamp": message.record["time"].isoformat(),
        "extra": message.record["extra"],
    }
    try:
        url = logsip
        endpoint = "/"
        headers = {"Content-type": "application/json"}
        conn = http.client.HTTPConnection(url, timeout=0.05)
        conn.request("POST", endpoint, json.dumps(log_entry, ensure_ascii=False).encode("utf-8"), headers)
    except Exception as e:
        # 如果远程日志失败，可以回退到本地日志
        qWarning(f"Failed to send log to remote: {str(e)}")


# 尝试添加post日志
try:
    headers = {"Content-type": "application/json"}
    conn = http.client.HTTPConnection(logsip, timeout=0.05)
    conn.request("POST", "/", json.dumps({"message": "add http log success"}, ensure_ascii=False).encode("utf-8"),
                 headers)
    log.add(post_to_remote, level="DEBUG")
except:
    pass


# 自定义日志处理函数
def qt_message_handler(mode, context, message):
    if mode == QtMsgType.QtInfoMsg:
        mode = "Info"
        log.info(f"{context.file}:{context.line}-->{mode}: {message}")
    elif mode == QtMsgType.QtWarningMsg:
        mode = "Warning"
        log.warning(f"{context.file}:{context.line}-->{mode}: {message}")
    elif mode == QtMsgType.QtCriticalMsg:
        mode = "Critical"
        log.critical(f"{context.file}:{context.line}-->{mode}: {message}")
    elif mode == QtMsgType.QtFatalMsg:
        mode = "Fatal"
        log.error(f"{context.file}:{context.line}-->{mode}: {message}")
    else:
        mode = "Debug"
        log.debug(f"{context.file}:{context.line}-->{mode}: {message}")


# 安装日志处理函数
qInstallMessageHandler(qt_message_handler)
###----------5、主体程序----------###

if __name__ == '__main__':
    qapp = QApplication(sys.argv)
    QQuickStyle.setStyle("Basic")

    cfgfile = 'config.json'
    if not os.path.exists(cfgfile):
        # 初始化配置
        cfg = {
            'id': uuid.uuid4().hex,
            'name': '后端模板',
            'author': "ROrange",
            'description': "模板-支持Py后端",
            'version': '4.0',
            'roversion': '4.0.0',  # RO启动器需要的最小版本
            "logo": "logo.png",
            "widget": "PySide6-QML"
        }
        with open(cfgfile, 'w', encoding='utf-8') as f:
            json.dump(cfg, f, ensure_ascii=False, indent=4)
    else:
        with open(cfgfile, 'r', encoding='utf-8') as f:
            cfg = json.load(f)
        # 配置修改
        cfg['version'] = '4.0'
        with open(cfgfile, 'w', encoding='utf-8') as f:
            json.dump(cfg, f, ensure_ascii=False, indent=4)

    # 创建QML引擎和组件
    engine = QQmlEngine()
    component = QQmlComponent(engine)

    widget = mainWindow(qapp, engine)

    for key, value in widget['property'].items():
        engine.rootContext().setContextProperty(key, value)

    component.loadUrl(QUrl.fromLocalFile(widget['qml']))

    qapp.setWindowIcon(QIcon(cfg['logo']))
    qapp.setApplicationDisplayName(cfg['name'])
    qapp.setApplicationName(cfg['id'])

    # 初始化QQuickWindow
    window = QQuickWindow()
    window.resize(350, 600)


    def handle_quit():
        log.debug("Received quit signal from QML")


    # 连接引擎的quit信号到处理函数
    engine.quit.connect(handle_quit)

    if component.isReady():
        # 创建QML根对象
        qml_object = component.create()
        if qml_object:
            # 将QML对象设置为窗口内容
            qml_object.setParentItem(window.contentItem())
            window.show()
        else:
            log.error("错误：无法创建QML组件")
            log.error(component.errorString())
            sys.exit(1)
    else:
        log.error("错误：QML组件加载失败")
        log.error(component.errorString())
        sys.exit(1)

    sys.exit(qapp.exec())