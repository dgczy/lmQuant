# -*- coding: utf-8 -*-
"""
判断运行环境
通过检测环境变量
"""

# 基本包

# try:
#     # 策略中必须导入kuanke.user_space_api包
#     from kuanke.user_space_api import *
# except:
#     pass

import numpy as np
import pandas as pd
import math
import os



# 日期时间
import time
from datetime import timedelta

IN_BACKTEST = False



# 检测文件
def exists_file(file_name):
    """
    研究中检测文件，使用os.path.exists函数
    file_name：文件名、含路径，str
    """
    return os.path.exists(file_name)


def get_volatility(df, years=None, days=30):
    """
    波动率
    df：数据表，df
    years：以年为单位的时段，int
    days：以年为单位的时段，int
    返回：波动率，float
    """
    # 按照年取数据
    if years is not None:
        start_date = df.index[-1].date() - timedelta(365 * years)
        df = df[df.index >= str(start_date)]

    # 按照天数取数据
    if days is not None:
        start_date = df.index[-1].date() - timedelta(days + 1)
        df = df[df.index >= str(start_date)]

    # 无数据返回Nan
    if len(df) == 0:
        return float(np.NaN)

    # 前一日收盘价
    df['pre'] = df.iloc[:, 0].shift(1)
    # 清除无效数据
    df = df.dropna()
    # 日收益率(当日收盘价/前一日收盘价，然后取对数)
    df['day_volatility'] = np.log(df['pre'] / df.iloc[:, 0])
    # 波动率（年化收益率的方差*sqrt(250)）
    volatility = df['day_volatility'].std() * math.sqrt(250.0) * 100

    # 返回值
    return round(volatility, 2)


def get_annualized(df, years=5):
    """
    年化回报率
    df：数据表，df
    years：以年为单位的时段，int
    返回：回报率，float
    """
    # 按照年取数据
    if years is not None:
        start_date = df.index[-1].date() - timedelta(365 * years)
        df = df[df.index >= str(start_date)]
    try:
        # 总收益率
        annualized = (df.iloc[:, 0][-1] - df.iloc[:, 0][0]) / df.iloc[:, 0][0]
        # 年化收益率
        annualized = (pow(1 + annualized, 250 / (years * 250.0)) - 1) * 100
    except:
        annualized = float(np.NaN)
    # 返回报率
    return round(annualized, 2)



# 对源数据按照周、月、年筛选
# period：D、W、M分别为日线、周线、月线
def data_to_period(df, period='W'):
    df['date'] = df.index
    df = df.resample(period).last()
    df.index = df['date']
    del df['date']
    df = df.dropna()
    df.index.name = None
    return df


# 四分位去除负值、极值
def data_del_IQR(p, k=0.5):
    # 去除负值
    x = np.array(p[p > 0])
    # 排序
    x = np.sort(x)
    # 取中值
    m = np.median(x)
    # 按照m分为两个数据表
    # 取小于m的数据表中值
    q1 = np.median(x[x <= m])
    # 取大于m的数据表中值
    q3 = np.median(x[x > m])
    # 计算上下临界值
    d = q1 - k * (q3 - q1)
    u = q3 + k * (q3 - q1)
    # 取大于d小于u且大于0的数据，并去除空值
    return p[(p > d) & (p < u) & (p > 0)].dropna()


# 四分位填充极值
def data_fill_IQR(p, k=0.734):
    x = np.array(p)
    x = np.sort(x)
    m = np.median(x)
    q1 = np.median(x[x <= m])
    q3 = np.median(x[x > m])
    d = q1 - k * (q3 - q1)
    u = q3 + k * (q3 - q1)
    p[p <= d] = d
    p[p >= u] = u
    return p


# 日期转换成时间戳
def date_to_timestamp(date):
    return int(time.mktime(time.strptime(date, '%Y-%m-%d')))


# 时间戳转换成日期
def timestamp_to_date(timestamp):
    return time.strftime('%Y-%m-%d', time.localtime(timestamp))

