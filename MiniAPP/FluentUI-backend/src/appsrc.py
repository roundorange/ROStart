#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###----------1、文件说明----------###
'''
* 说明：python程序模板
* 时间：
* 文件：
* 作者：Smile
* 版本：
 - 1.0 -> 2025-08-26 : 基础代码
    SHA256: A9217830632A76F04651AD7B002EBE5F87646971AF3DE40F81B84F75D3204980
 - 1.1 -> 2025-09-10 ：添加日志loginfo 变量属性
    SHA256: FDA211586E05DD52DBB2C4EBDE0C2A8D97FE4966035C0BC52272779579796A9D
 - 1.2 -> 2025-10-12 ：支持发送软件内通知消息
    SHA256: AD42E76BCA11EE2DA6557089701E612D2998C48983699C9054D2C7DB056DBA1E
* 备注：
'''
###----------2、库导入----------###
import os, sys
from PySide6.QtCore import QObject,Signal,Slot,Property
from loguru import logger as log
###----------3、参数配置----------###

###----------4、主体程序----------###

def pustWindowInfo(title="通知", text="信息", stime=0):
    '''
    在系统的通知栏，弹出一个信息(几秒钟后会自己没了）
    :param title: 通知的标题
    :param text: 通知的内容
    :param time: 多长时间后通知
    :return:
    '''
    # from win10toast import ToastNotifier
    log.debug(f"发送 {title} {text}")
    from win10toast_click import ToastNotifier
    import time
    toaster = ToastNotifier()

    time.sleep(stime)
    # toaster.show_toast(title, text, duration=10, threaded=True)
    toaster.show_toast(title, text)
    # while toaster.notification_active(): time.sleep(0.005)

class Backend(QObject):
    '''
    后端控制程序
    '''
    sigNotifyMessage = Signal(list)  # 通知消息
    def __init__(self, qapp):
        super().__init__()
        self.qapp = qapp
        self._text = "PySide6 QML APP"
        self._loginfo = ''

    # <---------- text属性管理 ---------->
    textChanged = Signal(str)
    def get_text(self):
        return self._text
    def set_text(self, value):
        self._text = value
        self.textChanged.emit(value)  # 属性变化时发射信号
    text = Property(str, get_text, set_text, notify=textChanged)

    # <---------- 日志信息管理 ---------->
    loginfoChanged = Signal(str)
    def get_loginfo(self):
        return self._loginfo
    def set_loginfo(self, value):
        self._loginfo += value + '\n'
        self.loginfoChanged.emit(value)  # 属性变化时发射信号
    loginfo = Property(str, get_loginfo, set_loginfo, notify=loginfoChanged)

    def sendNotifyMessage(self, title, message="", duration=1000, msgtype='success'):
        '''
        发送通知消息
        :param title: 要发送的消息
        :param message: 对消息的补充说明
        :param duration: 通知消息显示的时长（毫秒）
        :param msgtype: 消息类型 <success, info, warning, error>
        '''
        if msgtype in ['success', 'info', 'warning', 'error']:
            self.sigNotifyMessage.emit([title, message, duration, msgtype])
        pustWindowInfo(title, message)

    # 槽：供QML调用的方法
    @Slot(str, str)
    def debug(self, title, msgtype='success'):
        log.debug(f"QML msg: {title} {msgtype}")
        self.sendNotifyMessage(title,  msgtype=msgtype)

    # 槽：供QML调用的方法
    @Slot(str)
    def qmlCallback(self, message):
        log.debug(f"QML says: {message}")
