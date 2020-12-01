from django.http import HttpResponse, FileResponse, Http404
from django.shortcuts import render
import os, xlrd, xlsxwriter, zipfile
from django.conf import settings
from django.utils.encoding import escape_uri_path


# Create your views here.


# 　数据可视化视图函数
def data_visualization(request):
    if request.method == 'GET':
        return render(request, 'excel/data_visualization.html')
    elif request.method == 'POST':
        # 从前端获取用户上传的文件
        global File
        File = request.FILES.get("files", None)
        # print(File)
        # 调用文件上传函数获取文件
        upload_file(File)
        # 用户选择生成的图表
        user_choice = request.POST.get("choice_chart")
        # print(user_choice)
        # 要生成图表的数据、要处理的工作簿
        date_name = request.POST.get("data_name")
        sheet_index = int(request.POST.get('sheet_name'))
        # print(date_name)
        # print(sheet_name)
        # 调用获取数据的函数，获取用户上传表格中的需要生成图表的数据
        result = get_data(File, sheet_index, date_name)
        # 作为x轴的表头信息
        table_header = result[1]
        # 生成柱状图的数据
        date_list = result[0]

        if user_choice == 'bar_chart':
            # print(user_choice)
            # 调用生成柱状图的函数
            choice_chart = 'column'
            get_chart(File, date_list, table_header, choice_chart)

        elif user_choice == 'pie_chart':
            # print(user_choice)
            # 生成柱状图标的具体处理步骤
            choice_chart = 'pie'
            get_pie_chart(File, date_list, table_header, choice_chart)

        elif user_choice == 'line_chart':
            # print(user_choice)
            # 生成柱状图标的具体处理步骤
            choice_chart = 'line'
            get_chart(File, date_list, table_header, choice_chart)

        return render(request, 'excel/data_visualization.html')


# 文件上传功能
def upload_file(File):
    if File is None:
        return HttpResponse("请选择需要上传的文件")
    else:
        f = open(os.path.join(settings.BASE_DIR, File.name), 'wb')
        for chunk in File.chunks():
            f.write(chunk)
        f.close()


# 获取需要处理的数据函数
def get_data(File, sheet_index=0, date_name=None):
    """获取表数据"""
    results = []
    excel_book = xlrd.open_workbook(File.name)
    sheet = excel_book.sheet_by_index(sheet_index)
    ncols = sheet.ncols
    first_row = sheet.col_values(0)
    # print(first)
    for n in range(ncols):
        values = sheet.col_values(n)
        # print(values[0])
        if values[0] == date_name:
            results.append(values)
    results = results[0] if len(results) >= 1 else results
    # results.append(first_row)
    return results, first_row


# 生成柱状图和折线图函数
def get_chart(File, date_list, table_header, choice_chart):
    """写入一张新表,生成柱状图或折线图"""
    workbook = xlsxwriter.Workbook("{}_chart.xlsx".format(File.name.split('.')[0]))
    worksheet = workbook.add_worksheet()
    worksheet.write_column('A1', table_header)
    worksheet.write_column('B1', date_list)
    # 创建一个柱状图(column chart)
    chart_col = workbook.add_chart({'type': '{}'.format(choice_chart)})
    # 配置第一个系列数据
    name_len = len(table_header)
    values_len = len(date_list)
    chart_col.add_series({
        # 这里的sheet1是默认的值，因为我们在新建sheet时没有指定sheet名
        # 如果我们新建sheet时设置了sheet名，这里就要设置成相应的值
        'name': '=Sheet1!$B$1',
        'categories': '=Sheet1!$A$2:$A${}'.format(name_len),
        'values': '=Sheet1!$B$2:$B${}'.format(values_len),
        'line': {'color': 'red'},
    })
    # 设置图表的title 和 x，y轴信息
    chart_col.set_title({'name': '{}'.format(File.name)})
    chart_col.set_x_axis({'name': '员工信息'})
    chart_col.set_y_axis({'name': '数据'})
    # 设置图表的风格
    chart_col.set_style(1)
    # 把图表插入到worksheet以及偏移
    worksheet.insert_chart('E5', chart_col, {'x_offset': 5, 'y_offset': 5})
    workbook.close()


# 生成饼图函数
def get_pie_chart(File, date_list, table_header, choice_chart):
    """写入一张新表,生成饼图"""
    workbook = xlsxwriter.Workbook("{}_chart.xlsx".format(File.name.split('.')[0]))
    worksheet = workbook.add_worksheet()
    worksheet.write_column('A1', table_header)
    worksheet.write_column('B1', date_list)
    # 创建一个柱状图(column chart)
    chart_col = workbook.add_chart({'type': '{}'.format(choice_chart)})
    # 配置第一个系列数据
    name_len = len(table_header)
    values_len = len(date_list)
    chart_col.add_series({
        # 这里的sheet1是默认的值，因为我们在新建sheet时没有指定sheet名
        # 如果我们新建sheet时设置了sheet名，这里就要设置成相应的值
        'name': '=Sheet1!$B$1',
        'categories': '=Sheet1!$A$2:$A${}'.format(name_len),
        'values': '=Sheet1!$B$2:$B${}'.format(values_len),
        'line': {'color': 'red'},
    })
    # 设置图表的title 和 x，y轴信息
    chart_col.set_title({'name': '{}'.format(File.name)})
    chart_col.set_x_axis({'name': '员工信息'})
    chart_col.set_y_axis({'name': '数据'})
    # 设置图表的风格
    chart_col.set_style(10)
    # 把图表插入到worksheet以及偏移
    worksheet.insert_chart('E5', chart_col, {'x_offset': 5, 'y_offset': 5})
    workbook.close()


# 下载文件函数
# 文件传给前端下载
def file_iterator(file_path, chunk_size=512):
    """
    文件生成器,防止文件过大，导致内存溢出
    :param file_path: 文件绝对路径
    :param chunk_size: 块大小
    :return: 生成器
    """
    with open(file_path, mode='rb') as f:
        while True:
            c = f.read(chunk_size)
            if c:
                yield c
            else:
                break


# 将文件传输给前端提供给用户下载
def file_response_download(_):
    try:
        file_name = File.name.split('.')[0]
        # 压缩文件
        zip_file_path = './{}_chart.xlsx'.format(file_name)
        zip_file_name = './{}_chart.zip'.format(file_name)
        download_file_name = zip_file_name.split('/')[-1]
        fzip = zipfile.ZipFile(zip_file_name, 'w', zipfile.ZIP_DEFLATED)
        fzip.write(zip_file_path)
        fzip.close()
        # 将生成图表并压缩后的压缩包
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        file_path = os.path.join(base_dir, zip_file_name)
        response = FileResponse(open(file_path, 'rb'))
        response['content_type'] = "application/octet-stream"
        response['Content-Disposition'] = 'attachment; filename={}'.format(escape_uri_path(download_file_name))
        return response
    except Exception:
        raise Http404

#
# # 数据统计表视图函数
# def statistic_table(request):
#     if request.method == 'GET':
#         return render(request, 'excel/statistic_table.html')
#     elif request.method == 'POST':
#         # 从页面获取到用户需要统计的excel表
#         File = request.File.get('statistic_files', None)
#         upload_file(File)
#
#         # 从获取用户需要处理的数据
#         dispose_data = request.POST()
#
#         # 将用户选择的数据进行统计，写入一张新表中，返回页面中，提供给用户下载
#
#         return None  # 返回统计后的excel表格
#
#
# # 合并表格视图函数
# def combined_form(request):
#     if request.method == 'GET':
#         return render(request, 'excel/combined_form.html')
#     elif request.method == 'POST':
#         # 从页面获取用户多个excel表的压缩包
#
#         # 将文件解压，获取每一张excel表的数据，添加到一个新表中
#
#         return None  # 返回一张合并后的excel表提供用户下载
#
#
# # 拆分表格视图函数
# def table_split(request):
#     if request.method == 'GET':
#         return render(request, 'excel/table_split.html')
#     elif request.method == 'POST':
#         # 从页面获取用户需要处理的excel表
#
#         # 　将excel中的每条数据写入到一张新表中
#
#         return None  # 返回拆分的excel表的压缩包到页面给用户下载
