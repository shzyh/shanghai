# -*- coding: utf-8 -*-
# @Author: jiangfeng
# @Date:   2018-12-26 13:29:29
# @Last Modified by:   jiangfeng
# @Last Modified time: 2019-01-21 23:49:52

import pandas as pd
from db import database
from util import indictor


def strategy_30(df):
	f_close = df["f_close"]
	rsi1,rsi2,rsi3 = indictor.RSI(f_close)
	df['rsi1'] = rsi1
	df["rsi2"] = rsi2
	df["L20"] = 20
	df["H80"] = 80
	df["llv_low"] = indictor.LLV(df["f_low"],3)    #LLV(LOW,3)
	df["llv_rsi1"] = indictor.LLV(df["rsi1"],3)    #LLV(RSI1,3)
	df["llv_rsi2"] = indictor.LLV(df["rsi2"],6)    #LLV(RSI2,6)

	df["cross_rsi1_rsi2"] = indictor.CROSS(df["rsi1"],df["rsi2"])
	df["LLV_RSI2_21"] = map(lambda x: 1 if x<21 else 0 ,df["llv_rsi2"])

	df["cross_rsi2_20"] = indictor.CROSS(df["rsi2"],df["L20"])
	df["LOW_LLV"] = map(lambda x,y:1 if x==y else 0,df["f_low"],df["llv_low"])

	df["LLV_RSI1_20"] = map(lambda x:1 if x<20 else 0,df["llv_rsi1"])

	#买入条件1
	df["B_01"] = df["cross_rsi1_rsi2"]*df["LLV_RSI2_21"]

	#买入条件2
	df["B_02"] = df["cross_rsi2_20"]*df["LOW_LLV"]

	#买入条件3
	df["B_03"] = df["cross_rsi1_rsi2"]*df["LLV_RSI1_20"]

	df["B"] = map(lambda x,y,z:1 if (x+y+z)>0 else 0 ,df["B_01"],df["B_02"],df["B_03"])

	#卖出条件1
	# df["S_01"] = indictor.CROSS(df["H80"],df["rsi1"])
	df["S_01"] = indictor.CROSS(df["rsi1"],df["H80"])

	#卖出条件2
	# df["S_02"] = df["B"].shift(8)

	# df["S"] = map(lambda x,y:1 if x+y>0 else 0,df["S_01"],df["S_02"])
	df["S"] = df["S_01"]

	return df

def cmpt_point(df):
	B = 0
	S = 1

	items = []
	for i in range(len(df)):
		item = {}
		if df.at[i,"B"]==1:
		   	if S==1 and B==0:
		
				f_datetime = df.at[i,"f_datetime"]
				item["datetime"] = f_datetime
				item["index"] = i
				item["status"] = "B"
				item["close"] = df.at[i,"f_close"]
				item["date"] = df.at[i,"f_date"]
		
				# print u"买点时间：{}".format(f_datetime)
				B=1
				S=0
				items.append(item)
			else:
				pass
				# print u"索引{}的买点为重复买点".format(i)
			
		if df.at[i,"S"] == 1:
			if B==1 and S==0:

				f_datetime = df.at[i,"f_datetime"]
				item["datetime"] = f_datetime
				item["index"] = i
				item["status"] = "S"
				item["close"] = df.at[i,"f_close"]
				item["date"] = df.at[i,"f_date"]

				# print u"卖点时间：{}".format(df.at[i,"f_datetime"])
				B=0
				S=1
				items.append(item)
			else:
				pass
			# print u"索引{}的卖点为重复卖点".format(i)
	return pd.DataFrame(items)

def get_netValues(revenueValues):
    netv = 1
    netvs = []
    for rate in revenueValues:
        netv *= 1+rate
        netvs.append(netv)
    return netvs

def cmpt_stat(df,df_b_s):
	#计算每次交易的收益率
	df_b_s["pct_chg"] = df_b_s["close"].pct_change()  

	#提取每次卖出点的数据
	df_s = df_b_s.loc[1::2]

	#交易获正收益的数据
	df_up = df_s[df_s["pct_chg"]>0]

	#计算统计值
	stat = {}
	stat["test_sum"] = len(df)         #测试周期
	stat["trade_count"] = len(df_s)    #交易次数
	stat["revenue_count"] = df_up["pct_chg"].count()    #盈利次数
	stat["winrate"] = stat["revenue_count"]*1.0/stat["trade_count"]*100    #胜率
	stat["rev_max"] = df_s["pct_chg"].max()*100     #单次交易最大盈利
	stat["rev_min"] = df_s["pct_chg"].min()*100    #单次交易最大亏损
	stat["rev_sum"] = (get_netValues(df_s["pct_chg"].tolist())[-1]-1)*100   #总盈利

	return stat

def main():
	df_code = pd.read_excel("000300.xlsx",sheet_name="data")
	stock_codes = df_code["code"].tolist()
	stats = []
	bs = []
	for stock_code in stock_codes:
		print "in stock_code:{}".format(stock_code)
		df = pd.read_excel(r'data\30m\{}.xlsx'.format(stock_code),sheet_name="data")
		df = strategy_30(df)
		df_b_s = cmpt_point(df)
		df_b_s["stockcode"] = stock_code
		# print df_b_s
		bs.append(df_b_s)
		stat = cmpt_stat(df,df_b_s)
		stat["stock_code"] = stock_code
		stats.append(stat)
	df = pd.DataFrame(stats)
	df.to_excel("result300.xlsx",sheet_name="data")

	df_cmp_bs = pd.concat(bs)
	df_cmp_bs.to_excel("df_cmp_bs.xlsx",sheet_name="data")

	print df
	print "finished!"

if __name__ == '__main__':
	main()