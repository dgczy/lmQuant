
import numpy as np
import pandas as pd
import math
import os

try:
    # 聚源数据、交易日
    from jqdata import jy
except:
    pass

# 聚宽数据
import jqdatasdk
jqdatasdk.auth("13695683829", "ssk741212")
from jqdatasdk import *

# 日期时间
import time
from datetime import timedelta


def get_jq_divid(code, end_date):
    """
    指定日期股息率,jqdata版本
    code：股票代码,list or str
    end_date：截至日期
    返回：股息率、市值
    """
    # 判断代码是str还是list
    if not type(code) is list:
        code = [code]

    # 获取所有成份股派息总额
    # 数据表
    df = pd.DataFrame()
    # 因jqdata每次最多返回5000条数据，所以要多次查询
    # 偏移值
    offset = 0
    while True:
        #查询语句
        q = query(
            # 代码
            finance.STK_XR_XD.code,
            # 派息日期
            finance.STK_XR_XD.report_date,
            # 派息总额
            finance.STK_XR_XD.bonus_amount_rmb,
        ).filter(
            # 获取指定日期前所有分红
            finance.STK_XR_XD.report_date <= end_date,
            finance.STK_XR_XD.bonus_amount_rmb > 0,
            finance.STK_XR_XD.code.in_(code)
            # 偏移
        ).offset(offset)
        # 查询
        temp_df = finance.run_query(q)
        # 判断是否还有数据了
        if len(temp_df) == 0:
            break
        # 追加数据
        df = df.append(temp_df)
        # 偏 移值每次递增5000
        offset += 5000

    if len(df) == 0:
        div = float('NaN')
    else:
        # 生成排序字段
        df['sort'] = df['code'].astype('str') + df['report_date'].astype(
            'str').str[0:10]
        df = df.sort_values('sort')
        print(df)
        # 只保留最后一次派息数据
        df = df.drop_duplicates('code', keep='last')
        # 返回合计的派息数
        div = df['bonus_amount_rmb'].sum()

    # 获取指数总市值
    q = query(
        # 市值
        valuation.market_cap).filter(valuation.code.in_(code))
    # 获取各成份股市值(亿元)
    df = get_fundamentals(q, end_date)
    # 返回合计的成份股总市值（亿元）
    cap = df['market_cap'].sum()

    try:
        # 返回股息率
        return div / cap / 10000 * 100.0, cap
    except:
        return float('NaN'), float('NaN')





get_divid=get_jq_divid
print(get_jq_divid('600000.XSHG',"2020-01-14"))