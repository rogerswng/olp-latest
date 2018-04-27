# -*- coding: utf-8 -*-

"""

    基于连接池的数据库操作类
    Based on pymysql, DBUtils.PooledDB

"""

import pymysql
from pymysql.cursors import DictCursor
from DBUtils.PooledDB import PooledDB
import dbConfig


class Mysql(object):
    """
        MySQL 数据库连接对象，通过连接池实现
        Acquire connection: conn = Mysql.getConn()
        Release connection: conn.close() / del conn
    """
    # Connection Pool Object
    __pool = None

    def __init__(self):
        """
            构造数据库及连接池，从连接池取连接，并生成游标
        """
        # self._conn = pymysql.Connect(
        #     host=dbConfig.DBHOST,
        #     port=dbConfig.DBPORT,
        #     user=dbConfig.DBUSER,
        #     passwd=dbConfig.DBPSWD,
        #     db=dbConfig.DBNAME,
        #     charset=dbConfig.DBCHARSET
        #     )
        self._conn = self.__getConn()
        self._cursor = self._conn.cursor()

    @staticmethod
    def __getConn(self):
        """
            构造数据库连接池/获取连接
        """
        if Mysql.__pool is None:
            __pool = PooledDB(
                creator=pymysql,
                mincached=1,
                maxcached=20,
                host=dbConfig.DBHOST,
                port=dbConfig.DBPORT,
                user=dbConfig.DBUSER,
                passwd=dbConfig.DBPSWD,
                db=dbConfig.DBNAME,
                charset=dbConfig.DBCHARSET,
                cursorclass=DictCursor
            )
        return __pool.connection()

    def getAll(self, sql, params=None):
        """
            @Summary: 返回所有的查询结果
            @param sql: 查询的 sql 语句，有查询条件通过 params 参数传入
            @param params: tuple/dict 传入
            @return list/boolean
        """
        if params is None:
            count = self._cursor.execute(sql)
        else:
            count = self._cursor.execute(sql, params)

        if count>0:
            return self._cursor.fetchall()
        else:
            return False

    def getOne(self, sql, params=None):
        """
            @Summary: 返回第一条
            @param sql: 查询的 sql 语句，有查询条件通过 params 参数传入
            @param params: tuple/dict 传入
            @return list/boolean
        """
        if params is None:
            count = self._cursor.execute(sql)
        else:
            count = self._cursor.execute(sql, params)

        if count>0:
            return self._cursor.fetchone()
        else:
            return False

    def getSome(self, sql, num, params=None):
        """
            @Summary: 返回前 num 条
            @param sql: 查询的 sql 语句，有查询条件通过 params 参数传入
            @param num: 返回查询结果的条数
            @param params: 查询参数
            @return list/boolean
        """
        if params is None:
            count = self._cursor.execute(sql)
        else:
            count = self._cursor.execute(sql, params)

        if count>0:
            return self._cursor.fetchmany(num)
        else:
            return False

    def
