import os
import time

from pydocx import PyDocX
import time, zipfile


# def get_objects_outfile(obj, infile: str):
#     url_list = infile.split('x-x')
#     # if len(url_list) == 1:
#     #     dir, suffix = os.path.splitext(infile)
#     # else:
#     dir, suffix = os.path.splitext(url_list[0])
#     outfile = '{}x-x{}{}'.format(dir, obj, suffix)
#     return outfile

def get_objects_outfile(obj, infile: str):
    dir, suffix = os.path.splitext(infile)
    dir_list = infile.split('x-x')
    outfile = '{}x-x{}{}'.format(dir_list[0], obj, suffix)
    return outfile

def get_html_outfile(infile: str):
    dir, suffix = os.path.splitext(infile)
    outfile = '{}{}'.format(dir, '.html')
    return outfile


def docx_to_html(in_docx, out_html):
    html = PyDocX.to_html(in_docx)
    try:
        f = open(out_html, 'w', encoding="utf-8")
        f.write(html)
    except Exception as e:
        print("#######转换失败：%s" % e)
    finally:
        f.close()


def info_update(doc, old_info, new_info):
    '''此函数用于批量替换合同中需要替换的信息
    doc:文件
    old_info和new_info：原文字和需要替换的新文字
    '''
    result = False
    # 读取段落中的所有run，找到需替换的信息进行替换
    for para in doc.paragraphs:  #
        for run in para.runs:
            if old_info in run.text:
                run.text = run.text.replace(old_info, new_info)  # 替换信息
                result = True
    # 读取表格中的所有单元格，找到需替换的信息进行替换
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                if old_info in cell.text:
                    cell.text = cell.text.replace(old_info, new_info)  # 替换信息
                    result = True
    return result


def get_zip(files, zip_name):
    zp = zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED)
    for file in files:
        zp.write(file)
    zp.close()
    # time.sleep(5)
