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
* 备注：
'''
###----------2、库导入----------###
import os, sys
from PySide6.QtCore import QObject,Signal,Slot,Property,QSysInfo
from loguru import logger as log
###----------3、参数配置----------###
if QSysInfo.productType() == 'windows':
    pass

if QSysInfo.productType() == 'android':
    pass
###----------4、主体程序----------###
class Backend(QObject):
    '''
    后端控制程序
    '''
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

    def getROVersion(self):
        '''获取RO启动器的版本号'''
        if QSysInfo.productType() == 'android':
            from jnius import autoclass

            JavaPythonActivity = autoclass("org.kivy.android.PythonActivity")
            JavamActivity = JavaPythonActivity.mActivity

            APPNAME = JavamActivity.getPackageName()  # APP包名
            _PackageInfo = JavamActivity.getPackageManager().getPackageInfo(APPNAME, 0)
            APPLONGVERSION = _PackageInfo.versionName  # APP 长版本号
        else:
            APPLONGVERSION = "1.0.0"
        return APPLONGVERSION

    def compareVersion(self, version1, version2):
        '''
        比较两个版本号
        Args:
            version1: 新的版本号
            version2: 旧的版本号
        Returns: True(新版本号 >= 旧版本号) or False(新版本号 < 旧版本号)
        '''
        sver1 = version1.split('.') # 2.3.4
        sver2 = version2.split('.') # 1.2.3
        if sver1[0] > sver2[0]:
            return True
        elif sver1[0] < sver2[0]:
            return False
        else:
            if sver1[1] > sver2[1]:
                return True
            elif sver1[1] < sver2[1]:
                return False
            else:
                if sver1[2] > sver2[2]:
                    return True
                elif sver1[2] < sver2[2]:
                    return False
                else:
                    return True

    @Slot()
    def quitAPP(self):
        '''关闭APP前，一些数据的处理'''
        log.info(f"程序退出...")

        self.qapp.quit()

    # 槽：供QML调用的方法
    @Slot(str)
    def debug(self, msg):
        log.debug(f"QML msg: {msg}")
        ret = self.compareVersion("3.4.2", "3.4.5")
        log.debug(f"比较结果 {ret}")

    # 槽：供QML调用的方法
    @Slot(str)
    def qmlCallback(self, message):
        log.debug(f"QML says: {message}")
