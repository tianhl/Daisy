from __future__ import print_function

import Daisy
import pymysql
import json
class SvcTransSys(Daisy.Base.DaisySvc):

    def __init__(self, name):
        super().__init__(name)
        self.__con = None

    def initialize(self, host='192.168.212.204', user='root', password='123456_123', port=3306, db='HEPSbed', charset='utf8'):
        self.__con = pymysql.connect(host=host, user=user, password=password, port=port, db=db, charset=charset)
        self.__cur = self.__con.cursor()  
        return True

    def execute(self, table, data, doCommit = False):

        cols = ", ".join('`{}`'.format(k) for k in data.keys())
        val_cols = ', '.join('%({})s'.format(k) for k in data.keys())
        sql = "insert into "+table +" (%s) values(%s)"
        res_sql = sql % (cols, val_cols)
        print(res_sql)
        if doCommit:
            self.LogInfo("Insert SvcTransSys")
            self.__cur.execute(res_sql, data)
            self.__con.commit()
        else:
            print(data)
        return True

    def finalize(self):
        self.__cur.close()
        self.__con.close()
        return True






