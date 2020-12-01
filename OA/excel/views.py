import time

from django.http import JsonResponse
from django.shortcuts import render
from django.conf import settings
from tools.excel_analy import MyExcel
import os
# from urllib import parse

# Create your views here.
from tools.parse_zip import MyZip


def upload_excel(request):
    file = request.FILES.get('file')
    # print(settings.STATICFILES_DIRS[0]+'/a.xlsx')
    file_pwd = settings.STATICFILES_DIRS[0] + f'/{file.name}'
    if not file:
        result = {'code': 14001, 'error': '没有文件数据'}
        print(result)
        return JsonResponse(result)
    with open(file_pwd, 'wb') as f:
        for chunk in file.chunks():
            f.write(chunk)
    # 返回数据到页面　显示　['row''row']
    # 读取ｅｘｃｅｌ生成　列表
    excel_list_data = MyExcel().get_excel_data_list(filename = file_pwd)
    # print('>>>>>>>>>>>>ss:',excel_list_data)
    return JsonResponse({'code': 200,'data':{'lines_data':excel_list_data}})


def split(request):
    '''
    对 表格 进行拆分
    :param request:
    :return: 下载链接,和表单预览
    '''
    file = request.FILES.get('file')
    if not file:
        result = {'code': 14001, 'error': '没有文件数据'}
        print(result)
        return JsonResponse(result)
    file_pwd = settings.STATICFILES_DIRS[0] + f'/{file.name}'
    with open(file_pwd, 'wb') as f:
        for chunk in file.chunks():
            f.write(chunk)
    title_line = int(request.POST.get('title_line'))
    split_type = request.POST.get('split_type')
    print('title_line:',title_line)
    print('split_type:',split_type)
    if title_line <1:
        title_line = 1
    # 拆分表格 返回拆分后的excel 压缩包地址,和样本
    directory_name = file.name.split('.')[0]
    print(directory_name)
    result = MyExcel().split_excel(filename =file_pwd,title_line =title_line,split_type = split_type,directory_name=directory_name)

    zip_url = MyExcel().zip_file(directory=(settings.MEDIA_ROOT + '/' +directory_name))
    # %2f
    # result=parse.quote(zip_url)
    url = "127.0.0.1:8000/v1/downloads/zip/{}".format(zip_url)
    print(url)
    return JsonResponse({'code': 200, 'data': {'lines_data': result,'zip_url':url}})


def mergetable(request):
    '''
    合并列表
    :param request:
    :return:
    '''
    # 1 解压压缩包
    zip_file = request.FILES.get('file')
    title_line = int(request.POST.get('title_line'))
    print('title_line>>>>>>>>:',title_line)
    file_pwd = settings.MEDIA_ROOT + '/upload_zipfile' + f'/{zip_file.name}'
    if not os.path.exists(file_pwd):
        if not zip_file:
            result = {'code': 14001, 'error': '没有文件数据'}
            print(result)
            return JsonResponse(result)
        with open(file_pwd, 'wb') as f:
            for chunk in zip_file.chunks():
                f.write(chunk)
    end_dir = settings.MEDIA_ROOT + '/upload_zipfile'+ f'/{zip_file.name.split(".")[0]}'
    file_list = MyZip(zip_file =file_pwd,end_dir=end_dir).unzip()
    print('zippwd>>>:',file_list)
    # 2 合并表格,根据什么呢? 简单实现 表头 表内容
    tim = '-' + str(time.time())[8:13].replace('.', '')
    excelname = settings.MEDIA_ROOT + '/upload_zipfile'+'/'+zip_file.name.split(".")[0]+tim+'.xlsx'
    MyExcel().merge_excel(excelname =excelname ,exceldir=end_dir,excel_list=file_list,title_line = title_line)

    excel_list_data = MyExcel().get_excel_data_list(filename=excelname)
    # print('>>>>>>>>>>>>ss:',excel_list_data)
    url = "127.0.0.1:8000/v1/downloads/excel/upload_zipfile/{}".format(excelname.split('/')[-1])

    return JsonResponse({'code': 200, 'data': {'lines_data': excel_list_data,'zip_url':url}})



def upload_zip(request):
    file = request.FILES.get('file')
    # print(settings.STATICFILES_DIRS[0]+'/a.xlsx')
    file_pwd = settings.MEDIA_ROOT +'/upload_zipfile'+ f'/{file.name}'
    if not file:
        result = {'code': 14001, 'error': '没有文件数据'}
        print(result)
        return JsonResponse(result)
    with open(file_pwd, 'wb') as f:
        for chunk in file.chunks():
            f.write(chunk)


    # 返回数据到页面　显示　['row''row']
    # 读取ｅｘｃｅｌ生成　列表
    # excel_list_data = MyExcel().get_excel_data_list(filename = file_pwd)
    # print('>>>>>>>>>>>>ss:',excel_list_data)
    return JsonResponse({'code': 200})