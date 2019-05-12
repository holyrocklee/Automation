# coding=utf-8
import pymysql
import logging

from com.eason.util.excel_util import excelutil
from com.eason.util.file_util import fileutil

'''
       构建util
       util=mysql_util({'host':'127.0.0.1', 'user':'', 'passwd':'', 'db':''})
       执行sql,仅查看
       util.getData("sql")
       util.copy_to_text('select * from log_maintenance_result limit 100','d:/1.txt')
       util.copy_to_excel('select * from log_maintenance_result limit 100','d:/1.xls')
       关闭链接
       util.disconnect()
'''


class mysql_util:
    level = logging.DEBUG
    filename = None
    filemode = None

    def __init__(self, parameter, port=3306):
        logging.basicConfig(level=self.level, filename=self.filename, filemode=self.filemode,
                            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)
        self.connect = pymysql.Connect(host=parameter['host'], port=port, user=parameter['user'],
                                       passwd=parameter['passwd'], db=parameter['db'], charset='utf8')
        self.cursor = self.connect.cursor()

    def run(self, sql):
        self.sql = sql
        self.cursor.execute(sql)
        self.connect.commit()

    def getData(self, sql):
        self.run(sql)
        temp = []
        for row in self.cursor.fetchall():
            temp.append(row)
            self.logger.debug(row)
        return temp

    def disconnect(self):
        if self.cursor:
            self.cursor.close()
        if self.connect:
            self.connect.close()

    def copy_to_excel(self, sql, file=None):
        data = self.getData(sql)
        util = excelutil(file=file, mode='w')
        util.write_lines(data, save=True)

    def copy_to_text(self, sql, file):
        data = self.getData(sql)
        util = fileutil(file, mode='w', encoding='utf-8')
        util.writelines(data)
        util.close()


if __name__ == '__main__':
