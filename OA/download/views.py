from django.http import FileResponse, HttpResponse
from django.shortcuts import render
from django.conf import settings
# Create your views here.

def user_zip_download(request,filename):
    # return HttpResponse('ss')
    # 6月统计表-6月统计表.zip
    filename = filename.replace('-','/')
    # print(filename)
    print('user_download<<<<<<<<<<<',filename)
    filename = settings.MEDIA_ROOT+'/'+filename
    print(filename)
    file = open(filename,'rb')
    response = FileResponse(file)
    response['Content-Type']= 'application/octer-stream'
    file_name = filename.split('/')[-1]
    response['Content-Disposition']='attachment;filename={}'.format(file_name)
    return response


def test(request):
    return HttpResponse('test download')


def user_excel_download(request,filename):

    print('user_download<<<<<<<<<<<', filename)
    filename = settings.MEDIA_ROOT + '/upload_zipfile/'+ filename
    print(filename)
    file = open(filename, 'rb')
    response = FileResponse(file)
    response['Content-Type'] = 'application/octer-stream'
    file_name = filename.split('/')[-1]
    response['Content-Disposition'] = 'attachment;filename={}'.format(file_name)
    return response


def localtool_download(request):
    filename = settings.MEDIA_ROOT + '/localtool/localtool.zip'
    print(filename)
    file = open(filename, 'rb')
    response = FileResponse(file)
    response['Content-Type'] = 'application/octer-stream'
    file_name = filename.split('/')[-1]
    response['Content-Disposition'] = 'attachment;filename={}'.format(file_name)
    return response