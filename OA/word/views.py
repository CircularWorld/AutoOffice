import os
import time
import docx
from django.http import JsonResponse, FileResponse
from django.shortcuts import render
from django.views import View
from tools.image_tools import get_outfile
from tools.word_tools import get_html_outfile, docx_to_html, info_update, get_objects_outfile, get_zip
from .models import Words
from django.conf import settings
from pydocx import PyDocX


# Create your views here.


def word_view(request):
    return render(request, 'word/word_test.html')


def upload_view(request):
    if request.method != "POST":
        result = {'code': 401, 'error': 'Incorrect request method'}
        return JsonResponse(result)
    else:
        title = request.POST.get('title')
        data = request.FILES['file']
        try:
            f = Words.objects.create(title=title, file=data)
        except Exception as e:
            print("@@@@存储失败：%s" % e)
            return JsonResponse({'code': 501})
        docx_url = settings.MEDIA_URL + str(f.file)
        print('docx_url>>>>>',docx_url)
        # /media/file/04_Python高级_LNM4K6O.docx
        html_url = get_html_outfile(docx_url[1:])
        docx_to_html(docx_url[1:], html_url)

        new_url = '/' + html_url
        return JsonResponse({'code': 200, 'url': new_url})


def modify_view(request):
    if request.method != "POST":
        result = {'code': 401, 'error': 'Incorrect request method'}
        return JsonResponse(result)
    else:
        find_content = request.POST.get('find_content')
        modify_content = request.POST.get('replace_content')
        file = request.POST.get('file')
        url = settings.MEDIA_URL + file.split(settings.MEDIA_URL)[1]

        dir, suffix = os.path.splitext(url)
        docx_url = '{}{}'.format(dir, '.docx')
        # print('docx_url[1:]>>>>>>>>', docx_url[1:])
        # media/file/04_Python%E9%AB%98%E7%BA%A7_nRc4xg5.docx
        doc = docx.Document(docx_url[1:])
        if info_update(doc, find_content, modify_content):

            new_doc_url = get_outfile(docx_url[1:])
            doc.save(new_doc_url)

            html_url = get_html_outfile(new_doc_url)
            docx_to_html(new_doc_url, html_url)

            new_url = '/' + html_url
            return JsonResponse({'code': 200, 'url': new_url})
        else:
            return JsonResponse({'code': 200, 'url': url})


def batch_view(request):
    if request.method != "POST":
        result = {'code': 401, 'error': 'Incorrect request method'}
        return JsonResponse(result)
    else:
        old_obj = request.POST.get('old_obj')
        new_obj = request.POST.get('new_obj')
        file = request.POST.get('file')

        url = settings.MEDIA_URL + file.split(settings.MEDIA_URL)[1]
        dir, suffix = os.path.splitext(url)
        docx_url = '{}{}'.format(dir, '.docx')

        url_list = []
        obj_list = new_obj.split('/')
        for obj in obj_list:
            doc = docx.Document(docx_url[1:])
            info_update(doc, old_obj, obj)
            new_doc_url = get_objects_outfile(obj, docx_url[1:])
            doc.save(new_doc_url)

            html_url = get_html_outfile(new_doc_url)
            docx_to_html(new_doc_url, html_url)
            new_url = '/' + html_url
            url_list.append(new_url)
        return JsonResponse({'code': 200, 'url': url_list})


def download_view(request):
    file_list = request.GET.get('data').split(',')

    # 存储word文件地址列表
    docx_list = []
    for file in file_list:
        print("1111111111111", file)
        url = settings.MEDIA_URL + file.split(settings.MEDIA_URL)[1]
        dir, suffix = os.path.splitext(url)
        docx_url = '{}{}'.format(dir, '.docx')
        docx_list.append(docx_url[1:])

    print("222222222222222", docx_list)
    # 设置zip地址
    a_url = docx_list[0]
    dir, suffix = os.path.splitext(a_url)
    zip_url = '{}{}'.format(dir, '.zip')
    print("333333333333333333", zip_url)

    # 压缩word文件
    get_zip(docx_list, zip_url)

    # 下载文件
    a_file = open(zip_url, 'rb')
    response = FileResponse(a_file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="word.zip"'
    return response

