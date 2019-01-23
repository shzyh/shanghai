# -*- coding: utf-8 -*-
# @Author: jiangfeng
# @Date:   2018-11-22 17:13:08
# @Last Modified by:   jiangfeng
# @Last Modified time: 2018-12-24 09:11:23

import numpy as np
import pandas as pd


#取序列的绝对值
def ABS(series):
    return np.fabs(series)

#获取N日最大值序列
def HHV(series, N):
    return pd.Series.rolling(series, N).max()

#获取N日最小值序列
def LLV(series, N):
    return pd.Series.rolling(series, N).min()

#获取N日之和序列
def SUM(series, N):
    return pd.Series.rolling(series, N).sum()

#获取标准差序列
def STD(series, N):
    return pd.Series.rolling(series, N).std()

#IF函数,s1,s2数据格式为series
def IF(cond, s1, s2):
    return pd.Series(np.where(cond, s1, s2))
    
#cross函数
def CROSS(s1,s2):
	con1 = np.where(REF(s1,1)<REF(s2,1),1,0)
	con2 = np.where(s1>s2,1,0)
	return pd.Series(con1*con2)

#两个序列逐位比较，取其大者
def MAX(s1,s2):
	return np.maximum(s1,s2)


#两个序列逐位比较，取其小者
def MIN(s1, s2):
    return np.minimum(s1,s2)

#返回N之前的值序列，A数据格式为series
def REF(series,N):
	return series.shift(N)


def MA(series, N):
    return pd.Series.rolling(series, N).mean()


def EMA(series,N):
	res = np.nan_to_num(series).copy()
	for i in range(1,len(series)):
		res[i] = (res[i]*2+res[i-1]*(N-1))/(N+1)
	return pd.Series(res)


def SMA(series,N,M):
	res = np.nan_to_num(series).copy()
	for i in range(1,len(series)):
		res[i] = (res[i]*M+res[i-1]*(N-M))/N
	return pd.Series(res)


def ATR(C,H,L, N): 
    TR  = MAX(MAX((H - L), ABS(REF(C, 1) - H)), ABS(REF(C, 1) - L))
    ATR = MA(TR1, N)
    return ATR


def MACD(C, FAST=12, SLOW=26, MID=9):
    EMAFAST = EMA(C, FAST)
    EMASLOW = EMA(C, SLOW)
    DIFF = EMAFAST - EMASLOW
    DEA = EMA(DIFF, MID)
    MACD = (DIFF - DEA) * 2
    return DEA,DIFF,MACD


def KDJ(C,H,L, N=9, M1=3, M2=3):
    RSV = (C - LLV(L, N)) / (HHV(H, N) - LLV(L, N)) * 100
    RSV = RSV.replace([np.NaN],100)    #前几个值为NAN替换为100
    K = SMA(RSV, M1, 1)
    D = SMA(K, M2, 1)
    J = 3 * K - 2 * D
    return K,D,J


def OSC(C, N=20, M=6):  # 变动速率线
    OSC = (C - MA(C, N)) * 100
    MAOSC = EMA(OSC, M)
    return OSC,MAOSC
    

def BBI(C, N1, N2, N3, N4):  # 多空指标
    BBI = (MA(C, N1) + MA(C, N2) + MA(C, N3) + MA(C, N4)) / 4
    return BBI


def BBIBOLL(C, N1, N2, N3, N4, N, M):  # 多空布林线
    BBIBOLL = BBI(C, N1, N2, N3, N4)
    UPER = BBIBOLL + M * STD(BBIBOLL, N)
    DOWN = BBIBOLL - M * STD(BBIBOLL, N)
    return BBIBOLL,UPER,DOWN


def PBX(C, N1=4, N2=6, N3=9, N4=13, N5=18, N6=24):  # 瀑布线
    PBX1 = (EMA(C, N1) + EMA(C, 2 * N1) + EMA(C, 4 * N1)) / 3
    PBX2 = (EMA(C, N2) + EMA(C, 2 * N2) + EMA(C, 4 * N2)) / 3
    PBX3 = (EMA(C, N3) + EMA(C, 2 * N3) + EMA(C, 4 * N3)) / 3
    PBX4 = (EMA(C, N4) + EMA(C, 2 * N4) + EMA(C, 4 * N4)) / 3
    PBX5 = (EMA(C, N5) + EMA(C, 2 * N5) + EMA(C, 4 * N5)) / 3
    PBX6 = (EMA(C, N6) + EMA(C, 2 * N6) + EMA(C, 4 * N6)) / 3
    return PBX1,PBX2,PBX3,PBX4,PBX5,PBX6


def BOLL(C, N=20):  # 布林线
    MID = MA(C, N)
    UPER = MID + 2 * STD(C, N)
    DOWN = MID - 2 * STD(C, N)
    return MID,UPER,DOWN


def ROC(C, N=12, M=6):  # 变动率指标
    ROC = 100 * (C - REF(C, N)) / REF(C, N)
    MAROC = MA(ROC, M)
    return ROC,MAROC


def MTM(C, N, M):  # 动量线
    MTM = C - REF(C, N)
    MTMMA = MA(MTM, M)
    return MTM,MTMMA


def MFI(C,H,L,VOL, N):  # 资金指标
    TYP = (C + H + L) / 3
    V1 = SUM(IF(TYP > REF(TYP, 1), TYP * VOL, 0), N) / \
        SUM(IF(TYP < REF(TYP, 1), TYP * VOL, 0), N)
    MFI = 100 - (100 / (1 + V1))
    return MFI


def SKDJ(C,H,L, N, M):
    LOWV = LLV(L, N)
    HIGHV = HHV(H, N)
    RSV = EMA((C - LOWV) / (HIGHV - LOWV) * 100, M)
    RSV = RSV.replace([np.NaN],100)
    K = EMA(RSV, M)
    D = MA(K, M)
    return K,D


def WR(C,H,L, N1, N2):  # 威廉指标
    WR1 = 100 * (HHV(H, N1) - C) / (HHV(H, N1) - LLV(L, N1))
    WR2 = 100 * (HHV(H, N2) - C) / (HHV(H, N2) - LLV(L, N2))
    return WR1,WR2


def BIAS(C, N1, N2, N3):  # 乖离率
    BIAS1 = (C - MA(C, N1)) / MA(C, N1) * 100
    BIAS2 = (C - MA(C, N2)) / MA(C, N2) * 100
    BIAS3 = (C - MA(C, N3)) / MA(C, N3) * 100
    return BIAS1,BIAS2,BIAS3


def RSI(C, N1=6, N2=12, N3=20):  # 相对强弱指标
    LC = REF(C, 1)
    RSI1 = SMA(MAX(C - LC, 0), N1, 1) / SMA(ABS(C - LC), N1, 1) * 100
    RSI2 = SMA(MAX(C - LC, 0), N2, 1) / SMA(ABS(C - LC), N2, 1) * 100
    RSI3 = SMA(MAX(C - LC, 0), N3, 1) / SMA(ABS(C - LC), N3, 1) * 100
    return RSI1,RSI2,RSI3


# def RSI(C, N): 
#     LC = REF(C, 1)
#     RSI = SMA(MAX(C - LC, 0), N, 1) / SMA(ABS(C - LC), N, 1) * 100
#     return RSI

def ADTM(H,L,O, N, M):  # 动态买卖气指标
    DTM = IF(O <= REF(O, 1), 0, MAX(
        (H - O), (O - REF(O, 1))))
    DBM = IF(O >= REF(O, 1), 0, MAX((O - L), (O - REF(O, 1))))
    STM = SUM(DTM, N)
    SBM = SUM(DBM, N)
    ADTM = IF(STM > SBM, (STM - SBM) / STM,
               IF(STM == SBM, 0, (STM - SBM) / SBM))
    MAADTM = MA(ADTM, M)
    return ADTM,MAADTM


def DDI(H,L, N, N1, M, M1):  # 方向标准离差指数
    DMZ = IF((H + L) <= (REF(H, 1) + REF(L, 1)), 0,
             MAX(ABS(H - REF(H, 1)), ABS(L - REF(L, 1))))
    DMF = IF((H + L) >= (REF(H, 1) + REF(L, 1)), 0,
             MAX(ABS(H - REF(H, 1)), ABS(L - REF(L, 1))))
    DIZ = SUM(DMZ, N) / (SUM(DMZ, N) + SUM(DMF, N))
    DIF = SUM(DMF, N) / (SUM(DMF, N) + SUM(DMZ, N))
    DDI = DIZ - DIF
    ADDI = SMA(DDI, N1, M)
    AD = MA(ADDI, M1)
    return DDI,ADDI,AD


def DMI(C,H,L,N=14,M=6):
	TR  = SUM(MAX(MAX(H-L,ABS(H-REF(C,1))),ABS(L-REF(C,1))),N)
	# TR  = TR.replace([np.NaN],100)
	HD  = H-REF(H,1)
	LD  = REF(L,1) - L
	DMP = SUM(IF((HD > 0) & (HD > LD), HD,0), N)
	DMM = SUM(IF((LD > 0) & (LD > HD), LD,0), N)
	PDI = DMP*100 / TR
	MDI = DMM*100 / TR
	ADX = MA(ABS(MDI - PDI) / (MDI + PDI)*100,M)
	ADXR = (ADX + REF(ADX, M))/2
	return PDI,MDI,ADX,ADXR

def DMI_QL(C,H,L,N=14,M=6):
	TR  = SMA(MAX(MAX(H-L,ABS(H-REF(C,1))),ABS(L-REF(C,1))),N,1)
	HD  = H-REF(H,1)
	LD  = REF(L,1) - L
	DMP = SMA(IF((HD > 0) & (HD > LD), HD,0), N,1)
	DMM = SMA(IF((LD > 0) & (LD > HD), LD,0), N,1)
	PDI = DMP*100 / TR
	MDI = DMM*100 / TR
	ADX = SMA(ABS(MDI - PDI) / (MDI + PDI)*100,N,1)
	ADXR = (ADX + REF(ADX, M))/2
	return PDI,MDI,ADX,ADXR
