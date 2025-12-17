#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###----------1、文件说明----------###
'''
* 说明：http日志调试窗口
* 时间：2025-09-25
* 文件：
* 作者：ROrange
* 版本：0.1 显示http发送出来的日志
* 版本：0.2 可以将日志保存到文件中
    SHA256: 6D5B8216D1E0D6575CB898DCF71E0D4CD57175E03A4A45448D639D96D94DE2F5
* 版本：0.3 -> 2025-09-25 : 添加命令行配置选项。去除默认的日志内容，当post结果为200时，不显示，显示当前使用的IP
    SHA256: BC1DEB4E2F0D7EE070CAE4706CEB4FF6214BF799EBAA443A9FEC289FE09CD196
* 版本：0.4 -> 2025-11-16 ：支持显示模块名称，修复显示的bug
    SHA256: 380A61831131345CB3942C1AA39461DD418D39BCBCA394559FA01BEC457C1310
* 版本: 0.5 -> 2025-12-17: 发生错误时,显示空字符串 添加几个使用示例
    SHA256: 455570E3219F48D9BAE57832096B269E6130D0DEC0988ECF1F1EE75A56A25936
* 备注：
* 示例:
python logserver.py                      # 只显示基本信息  17:21:47.417 | ROStart  | INFO     | main.py:setWindowName:217 --> 启动程序 RO启动器
python logserver.py --thread             # 支持线程与进程信息显示
python logserver.py --time=date          # 显示日期与时间信息
python logserver.py --time=date --thread # 显示日期与时间信息 线程与进程信息显示
'''
###----------2、库导入----------###
import os, sys
from flask import Flask, request, jsonify
from loguru import logger
import logging
import argparse
from colorama import init, Fore, Back, Style
from pprint import pprint
import time
import traceback

init(autoreset=True)
###----------3、参数配置----------###
app = Flask(__name__)

class WerkzeugFilter(logging.Filter):
    def filter(self, record):
        # 过滤POST请求到根路径的日志
        if '"POST / HTTP/1.1" 200' in record.getMessage():
            return False
        return True

# 禁用Werkzeug默认的日志处理器
log = logging.getLogger('werkzeug')
log.setLevel(logging.INFO)
filter_instance = WerkzeugFilter()
log.addFilter(filter_instance)
# log.disabled = True

# 创建一个 ArgumentParser 对象
parser = argparse.ArgumentParser(
    description="""
日志输出格式，配置选项""",
    formatter_class=argparse.RawDescriptionHelpFormatter,add_help=False  # 禁用默认的help，使用自定义的
)

# 输出控制
output_group = parser.add_argument_group('程序配置')
output_group.add_argument('--thread', action='store_true', help='显示进程、线程信息')
output_group.add_argument('--time', type=str, default='time', choices=['date', 'time', 'none'], help='显示时间信息')
output_group.add_argument('--level', type=str, default='debug', choices=['debug', 'info', 'warning', 'error', 'critical'], help='显示日志等级')

# 信息选项
info_group = parser.add_argument_group('信息选项')
info_group.add_argument('--version', '-v',  action='version', version='%(prog)s 1.0.0', help='显示版本信息并退出')
info_group.add_argument('--help', '-h', action='help', default=argparse.SUPPRESS, help='显示帮助信息并退出')

# 解析命令行参数
args = parser.parse_args()

# 删除默认配置（可选）
logger.remove()

cmdformat = ""
if args.time == 'date':
    cmdformat += "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green>"
elif args.time == 'time':
    cmdformat += "<green>{time:HH:mm:ss.SSS}</green>"
elif args.time == 'none':
    cmdformat += ""

cmdformat += " | <cyan>{extra[mname]: <8}</cyan> | <level>{level: <8}</level> | "
cmdformat += "<cyan>{extra[cusfile]}</cyan>:<cyan>{extra[cusfunction]}</cyan>:<cyan>{extra[cusline]}</cyan>"

if args.thread:
    cmdformat += " - <cyan>{extra[cusprocess]}</cyan>:<cyan>{extra[custhread]}</cyan>"

cmdformat += " --> <level>{message}</level>"

logger.add(sys.stdout, format=cmdformat, level=args.level.upper(), colorize=True)
logger.add(
    "log/" + time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime()) + ".log",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
    rotation="10 MB",  # 日志轮转
    retention="30 days",  # 保留期限
    level="DEBUG"
)


###----------4、主体程序----------###
@app.route('/', methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])
def home():
    # pprint(request.json)
    jsondata = {}
    jsondata['file'] = request.json['file'] if "file" in request.json else "file.py"
    jsondata['function'] = request.json['function'] if "function" in request.json else "function"
    jsondata['line'] = request.json['line'] if "line" in request.json else "0"
    jsondata['process'] = request.json['process'] if "process" in request.json else "Process(0)"
    jsondata['thread'] = request.json['thread'] if "thread" in request.json else "Thread(0)"
    jsondata['mname'] = "APP"
    jsondata['message'] = str(request.json["message"]).replace("{", "{{").replace("}", "}}")

    if "extra" in request.json:
        if "name" in request.json["extra"]:
            jsondata['mname'] = request.json["extra"]["name"]

    if "level" not in request.json:
        try:
            logger.debug(jsondata['message'], cusfile=jsondata['file'], cusfunction=jsondata['function'], cusline=jsondata['line'], cusname=jsondata['process'],
                         custhread=jsondata['thread'], cusprocess=jsondata['process'], mname=jsondata['mname'])
        except:
            log.error(traceback.format_exc())
            if "message" in request.json:
                logger.debug("log info", cusfile=jsondata['file'], cusfunction=jsondata['function'],
                             cusline=jsondata['line'], cusname=jsondata['process'], custhread=jsondata['thread'],
                             cusprocess=jsondata['process'], mname=jsondata['mname'])
                print(jsondata['message'])
            else:
                print("-->", request.data)
        return 'Hello, Wlib'

    if request.json["level"] == "DEBUG":
        try:
            logger.debug(jsondata['message'], cusfile=jsondata['file'], cusfunction=jsondata['function'], cusline=jsondata['line'], cusname=jsondata['process'],
                         custhread=jsondata['thread'], cusprocess=jsondata['process'], mname=jsondata['mname'])
        except:
            logger.debug("", cusfile=jsondata['file'], cusfunction=jsondata['function'],
                         cusline=jsondata['line'], cusname=jsondata['process'], custhread=jsondata['thread'],
                         cusprocess=jsondata['process'], mname=jsondata['mname'])
            print("debug", jsondata['message'])
    elif request.json["level"] == "INFO":
        try:
            logger.info(jsondata['message'], cusfile=jsondata['file'], cusfunction=jsondata['function'], cusline=jsondata['line'], cusname=jsondata['process'],
                        custhread=jsondata['thread'], cusprocess=jsondata['process'], mname=jsondata['mname'])
        except:
            logger.info("", cusfile=jsondata['file'], cusfunction=jsondata['function'],
                         cusline=jsondata['line'], cusname=jsondata['process'], custhread=jsondata['thread'],
                         cusprocess=jsondata['process'], mname=jsondata['mname'])
            print(jsondata['message'])
    elif request.json["level"] == "WARNING":
        try:
            logger.warning(jsondata['message'], cusfile=jsondata['file'], cusfunction=jsondata['function'], cusline=jsondata['line'], cusname=jsondata['process'],
                           custhread=jsondata['thread'], cusprocess=jsondata['process'], mname=jsondata['mname'])
        except:
            logger.warning("", cusfile=jsondata['file'], cusfunction=jsondata['function'],
                         cusline=jsondata['line'], cusname=jsondata['process'], custhread=jsondata['thread'],
                         cusprocess=jsondata['process'], mname=jsondata['mname'])
            print(jsondata['message'])
    elif request.json["level"] == "ERROR":
        try:
            logger.error(jsondata['message'], cusfile=jsondata['file'], cusfunction=jsondata['function'], cusline=jsondata['line'], cusname=jsondata['process'],
                         custhread=jsondata['thread'], cusprocess=jsondata['process'], mname=jsondata['mname'])
        except:
            logger.error("", cusfile=jsondata['file'], cusfunction=jsondata['function'],
                         cusline=jsondata['line'], cusname=jsondata['process'], custhread=jsondata['thread'],
                         cusprocess=jsondata['process'], mname=jsondata['mname'])
            print(jsondata['message'])
    elif request.json["level"] == "CRITICAL":
        try:
            logger.critical(str(jsondata['message']), cusfile=jsondata['file'], cusfunction=jsondata['function'], cusline=jsondata['line'], cusname=jsondata['process'],
                            custhread=jsondata['thread'], cusprocess=jsondata['process'], mname=jsondata['mname'])
        except:
            logger.critical("", cusfile=jsondata['file'], cusfunction=jsondata['function'],
                         cusline=jsondata['line'], cusname=jsondata['process'], custhread=jsondata['thread'],
                         cusprocess=jsondata['process'], mname=jsondata['mname'])
            print(jsondata['message'])

    return 'Hello, Wlib'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=54444)
