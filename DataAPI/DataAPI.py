# -*- coding: utf-8 -*-
# @Author: jiangfeng
# @Date:   2019-01-17 10:16:45
# @Last Modified by:   jiangfeng
# @Last Modified time: 2019-01-18 14:08:53

import pandas as pd
import numpy as np
from datetime import datetime
from db import database
import confvar as cv

db = database.database()


class DataAPI(object):
	"""docstring for DataAPI"""
	def __init__(self, arg=None):
		self.arg = arg
		self.BEGIN_DATE_DEF = '20180101'
		self.END_DATE_DEF = '20181228'

	def get_mkt_equd(self,ticker=None,begin_date=None,end_date=None,field=None,adj=None,isopen=1):
		"""
			获取沪深股票日行情数据
			前复权：adj='qfq';后复权：adj='hfq';默认不复权
			默认返回：股票代码、交易日期、开盘价、最高价、最低价、收盘价、前收价、成交量、成交金额
		"""
		begin_date = self.BEGIN_DATE_DEF if begin_date is None else begin_date
		end_date = self.END_DATE_DEF if end_date is None else end_date

		if ticker is None:
			sql = "select * from t_stock_trade_ex where F_TRADE_DATE \
				between {} and {}".format(begin_date,end_date)
			items = db.fetch_all(sql)
		else:
			_ticker = ticker if isinstance(ticker,str) else ','.join(ticker)
			sql = "select * from t_stock_trade_ex where F_STOCK_STDCODE in ({}) and \
				F_TRADE_DATE between {} and {}".format(_ticker,begin_date,end_date)
			items = db.fetch_all(sql)

		if len(items)!=0:
			df = pd.DataFrame(items)
		else:
			print "return 0 record"
			return False

		if adj =="hfq":
			df["OPEN_ADJ"] = df["F_OPEN"]*df["F_EXRIGHT"]
			df["HIGH_ADJ"] = df["F_HIGH"]*df["F_EXRIGHT"]
			df["LOW_ADJ"]  = df["F_LOW"] *df["F_EXRIGHT"]
			df["CLOSE_ADJ"]= df["F_RERIGHT_AFT"]
			df["CLOSE_PRE_ADJ"] = df["F_PRECLOSE"]*df["F_EXRIGHT"]
			df["AVG_ADJ"] = df["F_AVG"] * df["F_EXRIGHT"]
			field = cv.FIELD_DEF_ADJ if field is None else field

		elif adj == "qfq":
			df["F_EXLEFT"] = df["F_EXRIGHT"].max()/df["F_EXRIGHT"]
			df["OPEN_ADJ"] = df["F_OPEN"]*df["F_EXLEFT"]
			df["HIGH_ADJ"] = df["F_HIGH"]*df["F_EXLEFT"]
			df["LOW_ADJ"]  = df["F_LOW"]*df["F_EXLEFT"]
			df["CLOSE_ADJ"]= df["F_CLOSE"]*df["F_EXLEFT"]
			df["CLOSE_PRE_ADJ"] = df["F_PRECLOSE"]*df["F_EXLEFT"]
			df["AVG_ADJ"]  = df["F_AVG"]*df["F_EXLEFT"]
			field = cv.FIELD_DEF_ADJ if field is None else field
		else:
			field = cv.FIELD_DEF if field is None else field

		#返回所有开盘交易的数据（除去停牌和非交易日数据）
		if isopen==1:
			df = df[df["F_STATUS"]==0]

		stockcode = df["F_STOCK_STDCODE"]		
		df = df.convert_objects(convert_numeric=True).round(2)
		df["F_STOCK_STDCODE"] = stockcode
		
		return df.loc[:,field]



