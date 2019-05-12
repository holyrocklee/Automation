# coding=utf-8
import os
import time
import sys
import logging
import math
import xlrd
import xlwt
from xlutils.copy import copy

class excelutil:
    '''

    写
    util = excelutil('d:/123.xls', 'w',head=['a','b']) 带表头的新表格，指定文件名
    util = excelutil(mode='w') 当前文件夹生成时间戳文件，不带表头

    util.write_line_by_nrow(0,[1,2,3,4]) 写在某行
    util.write_nextline([1,2,3,4],save=True) 自动写在下一行
    util.write_lines([[1,2],[1,2]],save=True) 一次写多行
    读
    util = excelutil('d:/123.xls', 'r') 文件必须存在
    util.read_lines_to_list_by_cols([0,1],2) 读1,2列数据,从第3行开始
    util.read_lines_to_list(2) 读所有列数据，从第3行开始
    util.read_lines_to_dic(1) 必须有表头，读所有列数据，返回[{head:value},{head:value}]格式数据，从第2列开始
    util.read_lines_to_dic_by_head(['a','b'],2) 必须有表头，读取指定列的数据，返回[{head:value},{head:value}]格式数据，从第3列开始
    util.read_all_sheet()
    追加
    util = excelutil(file='d:/1.xls', mode='a',index='a')
    util = excelutil('d:/a/b/12.xls', mode='a', head=[11, 12, 12, 12, 12, 12, 12, 12]) 文件必须传，可不存在
    util.write_nextline([0, 0, 0, 0, 0, 0, 0, 0])
    util.write_line_by_nrow(10, [1, 1, 1, 1, 1, 1, 1, 1])

    '''
    level = logging.DEBUG
    filename = None
    filemode = None

    def __init__(self, file=None, mode='r', index=0, head=None,encoding='utf-8'):
        logging.basicConfig(level=self.level, filename=self.filename, filemode=self.filemode,
                            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)
        # 读文件初始化
        if mode == 'r':
            self.read_mode(file, index=index)
        # 写文件初始化
        elif mode == 'w':
            self.write_mode(file, head=head,encoding=encoding)
        # 追加文件初始化
        elif mode == 'a':
            self.append_mode(file,index=index , head=head,encoding=encoding)
        else:
            raise Exception("excel 操作模式错误")

    '''
    ==============================以下为mode======================================
    '''

    '''
    读取excel初始化
    @:param file str 必须存在切以 xls或xlsx结尾
    @:param index int or str 读取的sheet id号或name，默认第1个sheet
    @:except
    '''
    def read_mode(self, file, index=0):
        if file and os.path.isfile(file) and (file.endswith('.xls') or file.endswith('.xlsx')):
            self.workbook = xlrd.open_workbook(file)
            if type(index) == int:
                self.table = self.workbook.sheet_by_index(index)
            elif type(index) == str:
                self.table = self.workbook.sheet_by_name(index)
        else:
            raise Exception("文件：" + file + "不存在或不是excel文件")

    '''
       写入excel初始化
       @:param file str 可以为None或者以xls
       @:param head [] 表头
       @:param encoding 字符编码
       @:param index 写入的sheet名称
       '''
    def write_mode(self, file=None, head=None, encoding='utf-8',index='sheet1'):
        if file:
            if file.endswith('.xls'):
                self.file = file
            else:
                self.logger.error(file+'不是xls文件')
                sys.exit()
        else:
            self.file = str(int(time.time())) + '.xls'
        # fileutil(self.file, 'w').close()

        self.row_num = 0
        self.workbook = xlwt.Workbook(encoding=encoding)
        self.table = self.workbook.add_sheet(index)
        if head:  # 有表头
            self.write_head(head)
            self.row_num = self.row_num + 1  # 写完表头行数自增

    '''
    追加模式
    @param file 表格文件，可以为None，必须是xls格式
    @param head 表头，只有在当前文件不存在，或者文件存在但是文件中无内容时起作用 []
    @param encoding 文件编码默认为utf-8
    @param index sheet的index或者名称 int or str
    '''

    def append_mode(self, file, head=None, encoding='utf-8', index=0):
        if file and os.path.isfile(file) and file.endswith('.xls'):
            self.file = file
            openworkbook = xlrd.open_workbook(file)
            sheet_names=openworkbook.sheet_names()
            self.workbook = copy(openworkbook)  # 用xlutils提供的copy方法将xlrd的对象转化为xlwt的对象
            if type(index) == int:
                try:
                    self.row_num = openworkbook.sheet_by_index(index).nrows  # 用wlrd提供的方法获得现在已有的行数
                except IndexError:
                    self.logger.error('append_mode: index 超出范围')
                    sys.exit()
                self.table = self.workbook.get_sheet(index)  # 用xlwt对象的方法获得要操作的sheet
            elif type(index) == str:
                try:
                    self.row_num = openworkbook.sheet_by_name(index).nrows
                except xlrd.biffh.XLRDError:
                    self.logger.error('sheet：'+index+' 不存在')
                    sys.exit()
                self.table = self.workbook.get_sheet(sheet_names.index(index))
            if head and self.row_num == 0:  # 写表头,文件存在但是要追加的sheet row_num为0
                self.write_head(head)
                self.row_num = self.row_num + 1
        else:
            self.write_mode(file, head, encoding,index)

    '''
    ===========================以下为读======================================
    '''

    ''' 
    读所有行返回二维数组
    @param    start int 起始行，默认从头开始
    @return result二维数组 [[1,2],[1,2]]
    '''

    def read_lines_to_list(self, start=0):
        rows = self.table.nrows
        result = []
        for i in range(start, rows):
            result.append(self.table.row_values(i))
            self.logger.debug(self.table.row_values(i))
        return result

    def read_lines_for_Multithreading(self):
        self

    '''
    读取整个excel
    @:return dict {'sheetname1':[{},{}],'sheetname2':[{},{}]}
    '''

    def read_all_sheet_to_dict(self):
        names = self.workbook.sheet_names()
        temp = {}
        for name in names:
            self.table = self.workbook.sheet_by_name(name)
            try:
                temp[name] = self.read_lines_to_dic()
                self.logger.debug('sheetname: ' + name)
                for x in temp[name]:
                    self.logger.debug(x)
            except IndexError:
                self.logger.warning('sheet：' + name + '中没数据')
        return temp

    '''
        读取整个excel
        @:return dict {'sheetname1':[[],[]],'sheetname2':[[],[]]}
    '''
    def read_all_sheet_to_list(self):
        names = self.workbook.sheet_names()
        temp = {}
        for name in names:
            self.table = self.workbook.sheet_by_name(name)
            temp[name] = self.read_lines_to_list()
            if len(temp[name]) > 0:
                self.logger.debug('sheetname: ' + name)
                for x in temp[name]:
                    self.logger.debug(x)
            else:
                temp.pop(name)
        return temp

    ''' 将表格处理成装字典的list，必须有表头的表格才能使用此方法，
        @param start 起始行默认从第2行开始
        @param Thread_count 读取线程，默认单线程
        
        @return l 如果thread_count=1 返回[{},{}],如果thread_count>1，返回[[{},{}],[{},{}]]
    '''

    def read_lines_to_dic(self, start=1, Thread_count=1):
        index = start
        heads = self.table.row_values(0)
        rows = self.table.nrows
        l = []
        for row in range(start, rows):
            values = self.table.row_values(row)
            dic = {}
            for key, col in zip(heads, range(len(heads))):
                dic[key] = values[col]
            dic['_index'] = index  # 每一行增加一个键值对  index=行号
            index = index + 1
            l.append(dic)
            self.logger.debug(dic)
        # 多线程读取
        if Thread_count > 1:
            l = self.slice_list(l, Thread_count)
        return l

    '''
    根据表头筛选数据
    @:param head ['',''] 字符数组，选择的列。如果选择的列表格中没有可以正常执行。
    @:param start 起始行，默认为1, 第1行为0。
    @:param Thread_count 分组数，默认为1
    
    @:return result Thread_count==1时:[{},{}] Thread_count>1时：[[{},{}],[{},{}]]
    '''

    def read_lines_to_dic_by_head(self, head, start=1, Thread_count=1):
        result = []
        rows = self.read_lines_to_dic(start=start, Thread_count=Thread_count)
        for row in rows:
            new_dic = {}
            # 分组数据
            if Thread_count > 1:
                new_list = []
                for r in row:
                    list_dic = {}
                    for h in head:
                        try:
                            list_dic[h] = r[h]
                        except KeyError:
                            self.logger.warning('read_lines_to_dic_by_head：表头不存在' + h)
                    list_dic['_index'] = r['_index']
                    new_list.append(list_dic)
                result.append(new_list)
                self.logger.debug(new_list)
            # 一组数据
            elif Thread_count == 1:
                for h in head:
                    new_dic[h] = row[h]
                self.logger.debug(new_dic)
                result.append(new_dic)
        return result

    '''
    根据列id读取表格中的数据
    @param cols list 需要取的列，第1列为0。如果该列超出范围则跳过该列 例：[0,2]
    @param start int 开始的行号，第1行为0
    
    @return l list [[],[]] 
    '''

    def read_lines_to_list_by_cols(self, cols, start=0):
        l = []
        for line in self.read_lines_to_list(start):
            new_line = []
            for index in cols:
                try:
                    new_line.append(line[index])
                except IndexError:
                    # index超出表格的范围
                    self.logger.warning('read_lines_to_list_by_cols：第' + str(index) + '列超出范围')
            l.append(new_line)
            self.logger.debug(new_line)
        return l

    '''
    ===================以下为写===============================
    '''

    '''
    根据行号写一行，并保存文件
    @:param row_name int 行号，第一行为0
    @:param row_value list [1,2,3]
    @:param save bool 
    '''
    def write_line_by_nrow(self, row_num, row_value,save=True):
        for value, col_num in zip(row_value, range(len(row_value))):
            self.table.write(row_num, col_num, value)
        self.logger.debug(row_value)
        if save:
            self.save()

    ''' 
    保存
    '''
    def save(self):
        try:
            self.workbook.save(self.file)
        except PermissionError:
            print("文件未关闭，或无保存权限")

    '''
    写下一行
    @:param row_value list [1,2,3]
    @:param save bool True保存 False不保存 默认保存
    '''
    def write_nextline(self, row_value,save=True):
        self.write_line_by_nrow(self.row_num, row_value,save=save)
        self.row_num = self.row_num + 1

    '''
    写多行 测试版本
    @:param data list 传入必须是[[1,2],[1,2]]格式
    @:param save bool True保存 False不保存 默认保存
    '''
    def write_lines(self, data,save=True):
        for values in data:
            if type(values) == tuple:
                values=list(values)
            if type(values) == list:
                self.write_nextline(values,save=save)
            else:
                self.logger.warning(values+' 不是list')
                continue
        if save:
            self.save()

    '''
       写表头
       @:param row_value list 传入必须是[1,2,3]格式
       @:param save bool True保存 False不保存 默认保存
    '''
    def write_head(self, row_value,save=True):
        self.write_line_by_nrow(0, row_value,save=save)

    '''
    将一个list均分成几个list便于多线程使用
    @param full_list 需要被切割的list
    @param count 切割的数量，不一定与设置的count完全一直。例：4条数据，切割成3个。只能切割成2个，每个数组2条数据
    @return [[],[]]
    '''
    def slice_list(self, full_list, count):
        result = []
        _len = len(full_list)
        # 向上取整
        every_list_len = math.ceil(_len / count)
        start_index = 0
        group_id = 1
        for x in range(count):
            temp = full_list[start_index:start_index + every_list_len]
            if len(temp) > 0:
                self.logger.debug('第' + str(group_id) + '组数据')
                group_id = group_id + 1
                for x in temp:
                    self.logger.debug(x)
            start_index = start_index + every_list_len
            result.append(temp)
        return result


if __name__ == '__main__':
    print(type((1,2)))