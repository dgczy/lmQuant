# -*- coding: utf-8 -*-


# 获取聚宽国际指数行情数据


# 包
import pandas as pd

# 聚宽数据
import jqdatasdk
jqdatasdk.auth("13695683829", "ssk741212")
from jqdatasdk import finance,query

#研究、策略中区别配置
try:
    #策略中必须导入kuanke.user_space_api包
    from kuanke.user_space_api import query
except:
    pass

_codes={
    'HSI':'800000.XHKG',#恒生国企指数
    'HSCEI':'800100.XHKG', #恒生国企指数   
    'HSCCI':'800151.XHKG', #恒生红筹指数
    'SPX':'INX', #标普500指数
    'NDAQ':'IXIC', #纳斯达克综合指数
    'DJIA':'DJI', #道琼斯指数
    'KS11':'KS11', #韩国综合指数
    'FTSE':'FTSE', #英国富时
    'RTS':'RTS', #俄罗斯RTS指数
    'MIB':'MIB', #意大利MIB指数
    'GDAXI':'GDAXI', #德国法兰克福DAX指数
    'N225':'N225', #东京日经225指数
    'IBEX':'IBEX', #西班牙IBEX35
    'FCHI':'FCHI', #法国巴黎CAC40指数
    'IBOV':'IBOV', #圣保罗IBOVESPA指数
    'MXX':'MXX', #墨西哥MXX指数
    'GSPTSE':'GSPTSE', #多伦多股票交易所综合
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
        code=_codes[code]

        # 今天日期
        today_str=pd.datetime.today().strftime('%Y-%m-%d')
        # 约束开始日期
        if start_date is None or start_date > today_str:
            start_date="1900-01-01"
        # 约束结束日期
        if end_date is None or end_date > today_str:
            end_date = today_str

        #数据表    
        df=pd.DataFrame()
        #因每次最多返回5000条数据，所以要多次查询
        #偏移值
        offset=0    
        while True:
            #查询语句
            q=query(
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
                finance.GLOBAL_IDX_DAILY.code==code,
                finance.GLOBAL_IDX_DAILY.day>=start_date,
                finance.GLOBAL_IDX_DAILY.day<=end_date,
            #偏移         
            ).offset(offset)
            #查询    
            temp_df=finance.run_query(q)  
            if len(temp_df)==0:
                break
            #追加数据
            df=df.append(temp_df)
            #偏移值每次递增5000    
            offset+=5000

        if len(df)==0:
            return None
        else:
            df.set_index("day",inplace=True)
            df.index.name=None
            return df

