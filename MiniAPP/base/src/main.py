#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###----------1、文件说明----------###
'''
* 说明：小程序基础模板
* 时间：2025-09-22
* 文件：
* 作者：ROrange
* 版本：
 - 0.1 -> : 小程序基础模板
* 备注：
'''
###----------2、库导入----------###
import os, sys
import json
import uuid,json
import http.client
from loguru import logger as log
from PySide6.QtWidgets import QApplication
from PySide6.QtQuick import QQuickWindow
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
            'name': '基础模板',
            'author': "ROrange",
            'description': "模板-小程序基础模板",
            'version': '1.0',
            'roversion': '1.0.0', # RO启动器需要的最小版本
            "logo": "logo.png",
            "widget": "PySide6-QML"
        }
        with open(cfgfile, 'w', encoding='utf-8') as f:
            json.dump(cfg, f, ensure_ascii=False, indent=4)
    else:
        with open(cfgfile, 'r', encoding='utf-8') as f:
            cfg = json.load(f)
        # 配置修改
        cfg['version'] = '1.0'
        with open(cfgfile, 'w', encoding='utf-8') as f:
            json.dump(cfg, f, ensure_ascii=False, indent=4)

    # 初始化QQuickWindow
    window = QQuickWindow()
    window.setTitle(cfg['name'])
    window.resize(350, 600)

    widget = mainWindow()

    def handle_quit():
        log.debug("Received quit signal from QML")

    # 连接引擎的quit信号到处理函数
    widget['engine'].quit.connect(handle_quit)

    if widget['component'].isReady():
        # 创建QML根对象
        qml_object = widget['component'].create()
        if qml_object:
            # 将QML对象设置为窗口内容
            qml_object.setParentItem(window.contentItem())
            # qml_object.setParent(window)
            # 自动调整窗口大小到根对象尺寸
            window.show()
        else:
            log.error("错误：无法创建QML组件")
            log.error(widget['component'].errorString())
            sys.exit(1)
    else:
        log.error("错误：QML组件加载失败")
        log.error(widget['component'].errorString())
        sys.exit(1)

    sys.exit(qapp.exec())