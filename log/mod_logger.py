# -*- coding: utf-8 -*-
# @Author: jiangfeng
# @Date:   2018-11-22 16:01:52
# @Last Modified by:   jiangfeng
# @Last Modified time: 2018-11-22 16:05:44
import logging
import os

DEBUG = os.getenv("YS_DEBUG","")

if DEBUG:
	LOG_LEVEL = logging.DEBUG
else:
	LOG_LEVEL = logging.INFO

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
# LOG_LEVEL = logging.DEBUG
# LOG_LEVEL = logging.ERROR

def logger(logpath):
	logging.basicConfig(filename=logpath,level=LOG_LEVEL,format=LOG_FORMAT)
	return logging
	pass

"""
日志级别
CRITICAL 50
ERROR    40
WARNING  30
INFO     20
DEBUG    10
NOSET    0
"""