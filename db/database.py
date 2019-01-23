# -*- coding: utf-8 -*-
# @Author: jiangfeng
# @Date:   2018-11-22 16:22:57
# @Last Modified by:   jiangfeng
# @Last Modified time: 2018-12-20 17:12:24

import pymysql
import mod_config
from log import mod_logger
import os

DB = "database"    #默认数据库
DBNAME = mod_config.getConfig(DB,"dbname")
DBHOST = mod_config.getConfig(DB,"dbhost")
DBUSER = mod_config.getConfig(DB,"dbuser")
DBPWD  = mod_config.getConfig(DB,"dbpwd")
DBCHARSET = mod_config.getConfig(DB,"dbcharset")
DBPORT = mod_config.getConfig(DB,"dbport")

log_path = os.path.join(os.getcwd()+r'\log','db_log.log')
logger = mod_logger.logger(log_path)


class database(object):
	def  __init__(self,dbname=None,dbhost=None,dbuser=None,dbpwd=None,dbport=None):
		self._logger = logger
		if dbname is None:
			self._dbname = DBNAME 
		else:
			self._dbname = dbname
		
		if dbhost is None:
			self._dbhost = DBHOST 
		else:
			self._dbhost = dbhost

		if dbuser is None:
			self._dbuser = DBUSER 
		else:
			self._dbuser = dbuser

		if dbpwd is None:
			self._dbpassword = DBPWD 
		else:
			self._dbpassword = dbpwd

		if dbport is None:
			self._dbport = int(DBPORT)
		else:
			self._dbport = dbport

		self._dbcharset  = DBCHARSET 

		self._conn = self.connectMySQL()

		if (self._conn):
			self._cursor = self._conn.cursor()

	#数据库连接
	def connectMySQL(self):
		conn = False
		try:
			conn = pymysql.connect(
					host    = self._dbhost,
					user    = self._dbuser,
					passwd  = self._dbpassword,
					db      = self._dbname,
					port    = self._dbport,
					charset = self._dbcharset,
					cursorclass = pymysql.cursors.DictCursor,
					)
		except Exception as e:
			self._logger.error("connect database failed, {}".format(e))
			conn = False
		return conn

	#获取查询结果集
	def fetch_all(self,sql,args=None):
		res = ''
		if (self._conn):
			try:
				if args == None:
					self._cursor.execute(sql)
				else:
					self._cursor.execute(sql,args)
				res = self._cursor.fetchall()
			except Exception as e:
				res = False
				self._logger.warn("query database exception:{}".format(e))
		return res

	#更新操作
	def update(self,sql,args=None):
		flag = False
		if (self._conn):
			try:
				self._cursor.execute(sql,args)
				self._conn.commit()
				flag = True
			except Exception as e:
				self._logger.warn("update database excetpion:{}".format(e))
		return flag
	
	#关闭数据库连接
	def close(self):
		if(self._conn):
			try:
				if (type(self._cursor)=='object'):
					self._cursor.close()
				if (type(self._conn)=='object'):
					self._conn.close()
			except Exception as e:
				self._logger.warn("close database exception:{},{},{}.".format(e,type(self._cursor),type(self._conn)))