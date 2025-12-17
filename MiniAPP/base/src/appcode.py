#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###----------1、文件说明----------###
'''
* 说明：程序代码，可由启动器启动。
*        python文件名不可变动
*        必须含有mainWindow，会被启动器调用
* 时间：2025-04-25 21:09:43
* 文件：
* 作者：ROrange
* 版本：
 - 1.0 -> 2025-04-25: 启动PySide6代码的启动代码，出错时会发送报错信息，并启动另一个界面，显示报错信息
    SHA256: AF59ECDE1AFB344A188E649A6DDD34C4333D1DB56740A9FF55A95F8FC211E5E6
* 备注：
'''
import os, sys
from PySide6.QtCore import QUrl
from PySide6.QtQml import QQmlEngine, QQmlComponent
from loguru import logger as log

def mainWindow():
    '''创建基于QML的类界面'''
    log.info("小程序启动")

    # 创建QML引擎和组件
    engine = QQmlEngine()
    component = QQmlComponent(engine)
    component.loadUrl(QUrl.fromLocalFile("main.qml"))

    widget = {
        'engine': engine,
        'component': component,
    }
    return widget
