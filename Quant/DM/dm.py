# -*- coding: utf-8 -*-
"""
功能：
    数据读写引擎
版本：
    v 0.1
说明：
    分为sqlite数据库版和cvs文件版
    两个版本的读写方法及参数、返回数据完全一致
"""

# 数据持久化包
import pickle

# 基本包
import pandas as pd

# 数据库包
from sqlalchemy import create_engine

print("数据引擎：准备好")


class Sqlite(object):
    """
    功能：数据库读写（sqlite）
    name：数据库名，str，如：‘idx_db’
    path：数据库路径，str，如：'data/'、‘../data/’
    """
    def __init__(self, name, path):
        self.__in_research = not IN_BACKTEST
        self.__name = name
        self.__path = path
        self.__connect = self.__connection()

    def __connection(self):
        """
        功能：连接数据库
        参数：无
        返回：数据库链接
        """
        # 直接连接数据库
        connect = create_engine('sqlite:///%s%s.db' %
                                (self.__path, self.__name))
        return connect

    def read(self, name, cols=None, parse_dates=False, encoding=None):
        """
        功能：读取数据
        name：表名，str，如：‘idx_000300’
        cols：字段名，list，如：[‘close’,'open']
        parse_dates：是否解析日期，bool
        encoding：编码格式，str
        返回：数据表，dataframe
        """
        # 修正parse_dates
        parse_dates = ['index'] if parse_dates else None
        # 从数据库中读取表，并重置索引
        df = pd.read_sql(name,
                         self.__connect,
                         columns=cols,
                         index_col='index',
                         parse_dates=parse_dates)
        df.index.name = None
        # 返回数据
        return df

    def save(self, name, df, append=True, encoding=None):
        """
        功能：保存数据到表、默认为追加模式
        name：表名，str
        df：数据表，dataframe
        append：追加、替换模式，bool
        encoding：编码格式，str
        返回：无
        """
        # 追加或替换
        exists = 'append' if append else 'replace'
        # code转换为表名，追加数据
        df.to_sql(name, self.__connect, if_exists=exists)

    def append(self, name, df):
        """
        功能：追加数据到表
        name：表名，str
        df：数据表，dataframe
        """
        # 追加数据
        self.save(name, df, True)

    def replace(self, name, df):
        """
        功能：替换数据表
        name：表名，str
        df：数据表，dataframe
        """
        # 替换数据
        self.save(name, df, False)


class Csv(object):
    """
    功能：CSV文件读写（研究环境 ）
    path：文件路径，str
    """

    # 构造行数
    def __init__(self, path=''):
        # 文件路径
        self.__path = path

    def read(self, name, cols=None, parse_dates=False, encoding=None):
        """
        功能：从csv文件读取数据
        name：表名，str，如：‘idx_000300’
        cols：字段名，list，如：[‘close’,'open']
        parse_dates：是否解析日期，bool
        encoding：编码格式，str
        返回：数据表，dataframe
        """
        # 使用cols时，默认不包括index列，所以必须加上index列
        # python3环境下，列表中不允许数字和字符串同时出现，所以出错
        # usecols = None if cols is None else [0] + cols

        # 读取cvs文件
        # df = pd.read_csv('%s%s.csv' % (self.__path, name),
        #                  usecols=usecols,
        #                  index_col=0,
        #                  parse_dates=parse_dates,
        #                  encoding=encoding)
        # cols不为空时，只能读取所有列，然后再取指定列
        if cols is None:
            df = pd.read_csv('%s%s.csv' % (self.__path, name),
                             index_col=0,
                             parse_dates=parse_dates,
                             encoding=encoding)
        else:
            df = pd.read_csv('%s%s.csv' % (self.__path, name),
                             index_col=0,
                             parse_dates=parse_dates,
                             encoding=encoding)[cols]
        # 返回数据表
        return df

    def save(self, name, df, append=True, encoding=None):
        """
        功能：保存数据到csv文件
        name：表名，str
        df：数据表，dataframe
        append：追加、替换模式，bool
        encoding：编码格式，str
        返回：无
        """
        # 修正追加或替换模式
        mode = 'a' if append else 'w'
        # 追加模式下不追加数据表头，替换模式使用数据表头
        header = False if append else True
        # 保存结果
        df.to_csv('%s%s.csv' % (self.__path, name),
                  mode=mode,
                  header=header,
                  encoding=encoding)


class Pickle(object):
    """
    功能：Pickle读写（研究环境 ）
    path：文件路径，str
    """

    # 构造行数
    def __init__(self, path=''):
        # 文件路径
        self.__path = path

    def read(self, name):
        """
        功能：读取pickle
        name：文件名，str
        返回：数据
        """
        with open('%s%s.pkl' % (self.__path, name), 'r') as pick_file:
            data = pickle.load(pick_file)
        return data

    def save(self, name, data):
        """
        功能：写入pickle
        name：文件名，str
        data：数据
        返回：无
        """
        with open('%s%s.pkl' % (self.__path, name), 'w') as pick_file:
            # 第三个参数必须为0
            pickle.dump(data, pick_file, 0)


class Image(object):
    """
    功能：图表保存为图像（研究环境 ）
    path：文件路径，str
    """
    def __init__(self, path=''):
        # 文件路径
        self.__path = path

    def save(self, fig, file_name, file_type='png'):
        """
        功能：图表保存为图像
        fig：图表画板对象
        file_name：文件名，str
        file_type：图像类型，即扩展名
        返回：无
        """
        # 文件全名
        file_name = self.__path + file_name + '.' + file_type
        # 使用画板对象的savefig方法生成图表为图像
        # 参数bbox_inches='tight'、,pad_inches=0必须，否则生成的图像有边框
        fig.savefig(file_name, dpi=fig.dpi, bbox_inches='tight', pad_inches=0)
