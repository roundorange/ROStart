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
 - 2.0 -> 2025-04-25: 启动PySide6代码的启动代码，出错时会发送报错信息，并启动另一个界面，显示报错信息
    SHA256: AF59ECDE1AFB344A188E649A6DDD34C4333D1DB56740A9FF55A95F8FC211E5E6
 - 2.1 -> 2025-10-12：添加后端类，供前端调用
    SHA256：0AD9946E1C75021DF29D7FF8FE42676E9FACFCE67E828A388ADC7F7A76C6A5E2
 - 2.2 -> 2026-03-04：添加传入参数app、engine。
    SHA256: B6217E3B62F2911344651602C1F2A0DBD53F68AC021ED713EBB7BE7FBB8615D1
* 备注：
'''
import os, sys
from loguru import logger as log
from FluentUI import FluentUI

def mainWindow(app, engine):
    '''创建基于QML的类界面'''
    log.info("小程序启动")

    FluentUI.registerTypes(engine)

    widget = {
        'qml': "main.qml", # 主要的QML文件
        'property': {      # 要在qml中注册的属性
        },
    }
    return widget
