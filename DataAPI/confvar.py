# -*- coding: utf-8 -*-
# @Author: jiangfeng
# @Date:   2019-01-18 14:01:48
# @Last Modified by:   jiangfeng
# @Last Modified time: 2019-01-18 14:10:15

##一些常量##


#**************************日行情***********************************
#默认返回日行情数据的字段
FIELD_DEF = ["F_STOCK_STDCODE","F_TRADE_DATE","F_OPEN","F_HIGH",
					"F_LOW","F_CLOSE","F_PRECLOSE","F_VOLUME","F_AMOUNT"
		]

#默认返回复权日行情数据的字段
FIELD_DEF_ADJ = ["F_STOCK_STDCODE","F_TRADE_DATE","OPEN_ADJ","HIGH_ADJ",
					"LOW_ADJ","CLOSE_ADJ","CLOSE_PRE_ADJ","F_AMOUNT"
		]

#**************************周行情***********************************