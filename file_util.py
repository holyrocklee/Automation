# coding=utf-8
import os
import sys

import logging

"""
文件工具类，支持 r，a，w 三种mode，读文件必须存在，写文件可不存在
encoding需要时指定

读
util=fileutil("d:/2.txt")
lines=util.readlines()

写
util=fileutil("d:/2.txt",'w')
util.writeline("line")
util.close()

追加
util=fileutil("d:/2.txt",'a')
util.writeline("line")
util.close()


"""


class fileutil:
    level = logging.DEBUG
    filename = None
    filemode = None

    # 初始化文件
    def __init__(self, file, mode='r', encoding=None):
        logging.basicConfig(level=self.level, filename=self.filename, filemode=self.filemode,
                            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)
        if mode == 'r':
            if not os.path.isfile(file):
                self.logger.info("文件：" + file + "不存在")
                sys.exit()
        elif mode == 'a' or mode == 'w':
            if not os.path.isdir(os.path.dirname(file)):
                try:
                    os.makedirs(os.path.dirname(file))
                except FileNotFoundError:
                    self.logger.info('文件路径' + file + '有误')
                    sys.exit()
        else:
            self.logger.info("mode=" + mode + " error")
            sys.exit()
        self.file_object = open(file, mode=mode, encoding=encoding)

    # 读取所有行
    # 如果文件不存在返回None
    def readlines(self):
        lines = self.file_object.readlines()
        self.close()
        for x in lines:
            self.logger.debug(x)
        return lines

    # 写一行
    def writeline(self, line):
        if type(line) == str:
            self.logger.debug(line)
            self.file_object.write(line + '\n')

    # 写数组
    def writelines(self, lines):
        if type(lines) == list:
            for line in lines:
                self.logger.debug(str(line))
                self.writeline(str(line))

    def close(self):
        self.file_object.close()


if __name__ == '__main__':
    util = fileutil('E:/projects/Automation/webAutomation.xlsx', encoding='utf-8')
    util.readlines()
    util.close()
