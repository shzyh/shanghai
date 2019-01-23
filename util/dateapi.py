# -*- coding: utf-8 -*-
# @Author: jiangfeng
# @Date:   2019-01-22 10:26:12
# @Last Modified by:   jiangfeng
# @Last Modified time: 2019-01-22 17:16:16

from datetime import datetime
from WindPy import w

w.start()

class DateApi(object):
	"""docstring for date"""
	def __init__(self):
		self.end_date = datetime.now().strftime('%Y%m%d')
		pass
	
	def get_tdays(self,begin_date=None,end_date=None,cycle="",style=""):
		"""
			获取日期序列
			输入参数：
				begin_date	起始日期 yyyymmdd或者yyyy-mm-dd
				end_date	截止日期
				cycle		周期 {默认为日，
									周：W；月：M；季：Q；年：Y}
				style		日期类型{默认为交易日，
									工作日：Weekdays；
									日历日：Alldays}
			函数返回: 
				返回begin_date和end_date之间复合条件的日期序列
				返回类型： yyyymmdd
		"""
		option = {"Days":style,"Period":cycle}
		end_date = self.end_date if end_date is None else end_date
		td = w.tdays(begin_date,end_date,**option)
		return [x.strftime('%Y%m%d') for x in td.Times]

	def get_tdays_offset(self,begin_date,offset,cycle="",style=""):
		"""
			获取偏移日期
			输入参数：
				begin_date	开始日期 yyyymmdd 或 yyyy-mm-dd
				offset 		偏移数量 -5表示往前5个日期；5表示往后5个日期
				cycle和style同get_tdays函数中
			函数返回：
				返回偏移N个周期的日期
				类型：yyyymmdd
		"""
		option = {"Days":style,"Period":cycle}
		td = w.tdaysoffset(offset,begin_date,**option)
		return td.Times[0].strftime("%Y%m%d")
		
	def get_tdays_count(self,begin_date,end_date,style=""):
		"""
			获取日期间的周期数
			输入参数：
				begin_date 	起始日期
				end_date 	截止日期
				style		日期类型
			函数返回：
				返回周期数N
				返回类型：int
		"""
		option = {"Days":style}
		td = w.tdayscount(begin_date,end_date,**option)
		return td.Data[0][0]