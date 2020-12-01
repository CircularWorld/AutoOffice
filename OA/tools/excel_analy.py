import time
import zipfile

import xlrd
import xlwt
import openpyxl
from xlutils.copy import copy
from django.conf import settings
import os


# 返回　excel 每行 列表[[],[],[]]

class MyExcel:
    def get_excel_data_list(self, filename):
        tmp_excel = xlrd.open_workbook(filename, formatting_info=False)
        table = tmp_excel.sheet_by_index(0)
        list_data = []
        r = 0
        while True:
            line_data = {}
            try:
                if not table.row(r):
                    break
            except IndexError:
                break
            # list_data.append(table.row_values(i))
            for c, item in enumerate(table.row_values(r)):
                line_data[c] = item
            r += 1
            list_data.append(line_data)
        # print(list_data)
        # [['小花公司6月入库统计表', '', '', ''],
        # ['客户名称', '次数', '重量（吨）', '总价'],
        # ['北大荒集团', '', '', ''],
        # ['小泽谷业专营', '', '', ''],
        # ['中粮集团', '', '', ''],
        # ['华夏粮油', '', '', ''],
        # ['北方粮油公司', '', '', ''],
        # ['四川粮配', '', '', '']]
        return list_data

    def split_excel(self, filename, title_line, split_type, directory_name):
        '''

        :param filename:
        :param title_line: 标题行
        :param split_type: 分类字段
        :return:
        '''
        title_line = title_line - 1
        tmp_excel = xlrd.open_workbook(filename, formatting_info=False)
        table = tmp_excel.sheet_by_index(0)
        split_type_is_exist = False
        # 字段所在行 用于生成文件名
        type_name_clum = 0
        if split_type:
            #     分割每一行
            try:
                if table.row(title_line):
                    for c, item in enumerate(table.row_values(title_line)):
                        if split_type == item:
                            print(item)
                            # 找到分类字段
                            type_name_clum = c
                            split_type_is_exist = True
                            break
                        else:
                            type_name_clum = 0
            except IndexError:
                print('没找到')

        #     分割每一行
        # 找到标题行
        # title_line_data = table.row_values(title_line)
        r = title_line + 1
        # 生成文件夹
        if not os.path.exists(settings.MEDIA_ROOT + '/' + directory_name):
            os.mkdir(settings.MEDIA_ROOT + '/' + directory_name)
        # 每次清空 数据 保留 压缩包
        for file in os.listdir(settings.MEDIA_ROOT + '/' + directory_name):
            # print(file)
            if not file.endswith('.zip'):
                os.remove(settings.MEDIA_ROOT + '/' + directory_name + '/' + file)
        while True:
            try:
                if not table.row(r):
                    break
            except IndexError:
                break
            # 生成 新的excel 写入 title 和 一行数据
            # list_data.append(table.row_values(i))

            # 生产工作簿
            new_excel = xlwt.Workbook()
            # 添加工作表
            new_table = new_excel.add_sheet('sheet1')
            # 写入内容
            for c, item in enumerate(table.row_values(title_line)):
                new_table.write(0, c, item)

            for c, item in enumerate(table.row_values(r)):
                new_table.write(1, c, item)
            # 保存工作簿 这个模块支持xls
            print('MMMMMMM',type_name_clum)
            file_pwd = settings.MEDIA_ROOT + '/' + directory_name + '/' + str(table.row_values(r)[type_name_clum]) + '.xlsx'
            print('file_pwd::',file_pwd)
            if os.path.exists(file_pwd):
                # 50.33
                tim = '-' + str(time.time())[8:13].replace('.', '')
                file_pwd = settings.MEDIA_ROOT + '/' + directory_name + '/' + str(table.row_values(r)[
                    type_name_clum]) + tim + '.xlsx'
            # print('file_pwd:::', file_pwd)
            new_excel.save(file_pwd)
            r += 1
        # self.zip_file(directory=(settings.MEDIA_ROOT + '/' + directory_name))
        return self.get_excel_data_list(
            settings.MEDIA_ROOT + '/' + directory_name + '/' + str(table.row_values(title_line + 1)[
                type_name_clum]) + '.xlsx')

    def merge_excel(self,excelname,exceldir,excel_list,title_line):
        # 我需要 合并后的excelname  读取每个excel的北荣 写入新的表excelname
        # excelname , 加上时间戳 防止覆盖
        # 1 创建新的 excel
        new_workbook = xlwt.Workbook()
        # 添加工作表
        worksheet = new_workbook.add_sheet("sheet1")
        # 遍历 excel
        row = 1
        if title_line<1:
            title_line = 1
        for excel in excel_list:
            excel_pwd =exceldir+'/'+ excel
            temp_excel = xlrd.open_workbook(excel_pwd)
            temp_sheet = temp_excel.sheet_by_index(0)
            temp_row = title_line

            while True:
                try:
                    if temp_sheet.row_values(temp_row):
                        for c, item in enumerate(temp_sheet.row_values(temp_row)):
                            worksheet.write(row, c, item)
                            temp_row+=1
                        row+=1
                except IndexError:
                    break
        # 表头
        excel_pwd = exceldir + '/' + excel_list[0]
        temp_excel = xlrd.open_workbook(excel_pwd)
        temp_sheet = temp_excel.sheet_by_index(0)
        try:
            if temp_sheet.row_values(title_line-1):
                for c, item in enumerate(temp_sheet.row_values(title_line-1)):
                    worksheet.write(0, c, item)
        except IndexError:
             pass


        # 保存工作簿 这个模块支持xls
        new_workbook.save(excelname)



    def zip_file(self, directory:str):
        '''
        返回 压缩包地址
        :param directory:
        :return:
        '''
        zipname = (directory+'/'+directory.split('/')[-1]+'.zip')
        zipFile = zipfile.ZipFile(zipname, 'w')
        for file in os.listdir(directory):
            if not file.endswith('.zip'):

                zipFile.write((directory+'/' + file), file, zipfile.ZIP_DEFLATED)
                # 压缩后删除
                os.remove(directory+'/' + file)
                # print('OK ??????????????')
        # print(zipFile.filelist)
        zipFile.close()
        # /home/tarena/project/office_auto_v1.0/OA/media/6月统计表/6月统计表.zip

        return zipname.split('/')[-2]+'-'+zipname.split('/')[-1]


