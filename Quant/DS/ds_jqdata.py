# -*- coding: utf-8 -*-
"""
聚宽数据源
"""

# 基本包
import pandas as pd

# 聚宽数据
import jqdatasdk
jqdatasdk.auth("13695683829", "ssk741212")
from jqdatasdk import *

try:
    # 聚源数据、交易日
    from jqdata import jy
except:
    pass


def __get_jq_divid(code, end_date):
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


def __get_jy_divid(code, end_date):
    """
    指定日期股息率,jy版本
    code：股票代码,list or str
    end_date：截至日期
    返回：股息率、市值
    """
    # 判断代码是str还是list
    if not type(code) is list:
        code = [code]

    # 聚宽代码转换为jy内部代码
    InnerCodes = Code.stk_to_jy(code)
    # 获取所有成份股派息总额
    # 数据表
    df = pd.DataFrame()
    # 因jy每次最多返回3000条数据，所以要多次查询
    # 偏移值
    offset = 0
    while True:
        # 查询语句
        q = query(
            # 内部代码
            jy.LC_Dividend.InnerCode,
            # 派息日期
            jy.LC_Dividend.ToAccountDate,
            # 派息总额
            jy.LC_Dividend.TotalCashDiviComRMB,
        ).filter(
            # 已分红
            jy.LC_Dividend.IfDividend == 1,
            # 获取指定日期前所有分红
            jy.LC_Dividend.ToAccountDate <= end_date,
            jy.LC_Dividend.InnerCode.in_(InnerCodes)
            # 偏移
        ).offset(offset)
        # 查询
        temp_df = jy.run_query(q)
        if len(temp_df) == 0:
            break
        # 追加数据
        df = df.append(temp_df)
        # 偏移值每次递增3000
        offset += 3000

    if len(df) == 0:
        div = float('NaN')
    else:
        # 生成排序字段
        df['sort'] = df['InnerCode'].astype(
            'str') + df['ToAccountDate'].astype('str').str[0:10]
        df = df.sort('sort')
        # 只保留最后一次派息数据
        df = df.drop_duplicates('InnerCode', take_last=True)  # keep='last'
        # 返回合计的派息数
        div = df['TotalCashDiviComRMB'].sum()

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
        return div / cap / 100000000 * 100.0, cap
    except:
        return float('NaN'), float('NaN')


get_divid = __get_jq_divid

codes = {
    'HSI': '800000.XHKG',  #恒生国企指数
    'HSCEI': '800100.XHKG',  #恒生国企指数   
    'HSCCI': '800151.XHKG',  #恒生红筹指数
    'SPX': 'INX',  #标普500指数
    'NDAQ': 'IXIC',  #纳斯达克综合指数
    'DJIA': 'DJI',  #道琼斯指数
    'KS11': 'KS11',  #韩国综合指数
    'FTSE': 'FTSE',  #英国富时
    'RTS': 'RTS',  #俄罗斯RTS指数
    'MIB': 'MIB',  #意大利MIB指数
    'GDAXI': 'GDAXI',  #德国法兰克福DAX指数
    'N225': 'N225',  #东京日经225指数
    'IBEX': 'IBEX',  #西班牙IBEX35
    'FCHI': 'FCHI',  #法国巴黎CAC40指数
    'IBOV': 'IBOV',  #圣保罗IBOVESPA指数
    'MXX': 'MXX',  #墨西哥MXX指数
    'GSPTSE': 'GSPTSE',  #多伦多股票交易所综合
}


class GIDX(object):

    # 获取聚宽国际指数行情数据
    @staticmethod
    def hist_price(code, start_date=None, end_date=None):
        """
        指定日期股息率,jy版本
        code：股票代码,list or str
        end_date：截至日期
        返回：股息率、市值
        """

        # 代码转换
        code = _codes[code]

        # 今天日期
        today_str = pd.datetime.today().strftime('%Y-%m-%d')
        # 约束开始日期
        if start_date is None or start_date > today_str:
            start_date = "1900-01-01"
        # 约束结束日期
        if end_date is None or end_date > today_str:
            end_date = today_str

        #数据表
        df = pd.DataFrame()
        #因每次最多返回5000条数据，所以要多次查询
        #偏移值
        offset = 0
        while True:
            #查询语句
            q = query(
                # 字段
                finance.GLOBAL_IDX_DAILY.day,
                finance.GLOBAL_IDX_DAILY.open,
                finance.GLOBAL_IDX_DAILY.close,
                finance.GLOBAL_IDX_DAILY.low,
                finance.GLOBAL_IDX_DAILY.high,
                #                 finance.GLOBAL_IDX_DAILY.volume,
                #                 finance.GLOBAL_IDX_DAILY.pre_close,
            ).filter(
                # 条件
                finance.GLOBAL_IDX_DAILY.code == code,
                finance.GLOBAL_IDX_DAILY.day >= start_date,
                finance.GLOBAL_IDX_DAILY.day <= end_date,
                #偏移
            ).offset(offset)
            #查询
            temp_df = finance.run_query(q)
            if len(temp_df) == 0:
                break
            #追加数据
            df = df.append(temp_df)
            #偏移值每次递增5000
            offset += 5000

        if len(df) == 0:
            return None
        else:
            df.set_index("day", inplace=True)
            df.index.name = None
            return df


class jqData(object):
    @staticmethod
    def hist_price(code,
                   start_date=None,
                   end_date=None,
                   period='D',
                   fields=None):
        """
        获取历史行情数据，限制开始、结束时间版本
        code：代码，str
        start_date：开始日期，str，如：'2018-07-01'
        end_date：结束日期，str，如：'2018-07-31'
        period：暂不支持
        """
        return get_price(code,
                         start_date=start_date,
                         end_date=end_date,
                         fields=fields)

    @staticmethod
    def security_info(code):
        """
        获取证券信息
        code：代码，str
        """
        return get_security_info(code)

    @staticmethod
    def index_stocks(code, end_date=None):
        """
        获取证券信息
        code：代码，str
        end_date：日期，str，如：'2018-07-01'
        """
        return get_index_stocks(code, date=end_date)

    @staticmethod
    def industries_stocks(code, end_date=None):
        """
        获取行业成分股
        code：代码，str
        end_date：日期，str，如：'2018-07-01'
        """
        return get_industry_stocks(code, date=end_date)

    @staticmethod
    def industries_list(code):
        """
        获取行业成分股
        code：代码，str
        """
        return get_industries(name='sw_l1')

    @staticmethod
    def fund_extras(code, start_date=None, end_date=None):
        """
        获取证券信息
        code：代码，str
        end_date：日期，str，如：'2018-07-01'
        """
        return get_extras('unit_net_value',
                          code,
                          start_date=start_date,
                          end_date=end_date)

    @staticmethod
    def trade_days(start_date=None, end_date=None, count=None):
        """
        获取证券信息
        code：代码，str
        end_date：日期，str，如：'2018-07-01'
        """
        return get_trade_days(start_date=start_date,
                              end_date=end_date,
                              count=count)


class Code(object):
    @classmethod
    def __secu_to_jq(cls, code):
        if code.endswith('SH'):
            return code.replace('SH', 'XSHG')
        if code.endswith('SZ'):
            return code.replace('SZ', 'XSHE')

    @classmethod
    def __jq_to_secu(cls, code):
        if code.endswith('XSHG'):
            return code.replace('XSHG', 'SH')
        if code.endswith('XSHE'):
            return code.replace('XSHE', 'SZ')

    @classmethod
    def secu_to_jq(cls, code):
        if type(code) is str:
            return cls.__secu_to_jq(code)
        elif type(code) is list:
            return [cls.__secu_to_jq(item) for item in code]

    @classmethod
    def jq_to_secu(cls, code):
        if type(code) is str:
            return cls.__jq_to_secu(code)
        elif type(code) is list:
            return [cls.__jq_to_secu(item) for item in code]

    @classmethod
    def __secu_to_jy(cls, codes, category=1):
        df = pd.DataFrame()
        # 因jy每次最多返回3000条数据，所以要多次查询
        # 偏移值
        offset = 0
        while True:
            q = query(
                # 内部代码
                jy.SecuMain.InnerCode, ).filter(
                    # 去除聚宽代码后缀
                    jy.SecuMain.SecuCode.in_(codes),
                    # 限定查询股票
                    jy.SecuMain.SecuCategory == category
                    # 偏移
                ).offset(offset)
            # 查询
            temp_df = jy.run_query(q)
            # 无数据时退出
            if len(temp_df) == 0:
                break
            # 追加数据
            df = df.append(temp_df)
            # 偏移值每次递增3000
            offset += 3000
        # 返回代码list
        return df.InnerCode.tolist()

    @classmethod
    def idx_to_jy(cls, code):
        if type(code) is str:
            return cls.__secu_to_jy([code[0:6]], category=4)[0]
        elif type(code) is list:
            return cls.__secu_to_jy([item[0:6] for item in code], category=4)

    @classmethod
    def stk_to_jy(cls, code):
        if type(code) is str:
            return cls.__secu_to_jy([code[0:6]], category=1)[0]
        elif type(code) is list:
            return cls.__secu_to_jy([item[0:6] for item in code], category=1)


