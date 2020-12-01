from django.http import JsonResponse, HttpResponse, FileResponse
from django.shortcuts import render
from django.conf import settings
from tools.image_tools import add_water, compress_image, cut_image
from image.models import Images


# Create your views here.
def image_views(request):
    if request.method == "GET":
        return render(request, 'image/index.html')


def upload_views(request):
    if request.method != "POST":
        result = {'code': 401, 'error': 'Incorrect request method'}
        return JsonResponse(result)
    else:
        title = request.POST.get('title')
        image = request.FILES['image']
        img = Images.objects.create(title=title, image=image, sign=True)
        url = settings.MEDIA_URL + str(img.image)
        return JsonResponse({'code': 200, 'title': img.title, 'url': url})


def water_views(request):
    if request.method != "POST":
        result = {'code': 401, 'error': 'Incorrect request method'}
        return JsonResponse(result)
    else:
        font_content = request.POST.get('font_content')
        font_size = request.POST.get('font_size')
        text_x = request.POST.get('text_x')
        text_y = request.POST.get('text_y')
        image = request.POST.get('image')

        o_url = settings.MEDIA_URL + image.split(settings.MEDIA_URL)[1]
        # 添加水印并返回地址
        url = add_water(o_url[1:], font_content, x=int(text_x), y=int(text_y), size=int(font_size))
        new_url = url.split('media/')[1]

        return JsonResponse({'code': 200, 'url': settings.MEDIA_URL + new_url})


def compress_views(request):
    if request.method != "POST":
        result = {'code': 401, 'error': 'Incorrect request method'}
        return JsonResponse(result)
    else:
        image = request.POST.get('image')
        str_proportion = request.POST.get('proportion')
        o_url = settings.MEDIA_URL + image.split(settings.MEDIA_URL)[1]
        proportion = float(int(str_proportion.split('%')[0]) / 100)

        # 压缩图片
        url = compress_image(o_url[1:], ratio=proportion)
        new_url = url.split('media/')[1]

        return JsonResponse({'code': 200, 'url': settings.MEDIA_URL + new_url})


def cut_views(request):
    if request.method != "POST":
        result = {'code': 401, 'error': 'Incorrect request method'}
        return JsonResponse(result)
    else:
        image = request.POST.get('image')
        left = request.POST.get('left')
        upper = request.POST.get('upper')
        right = request.POST.get('right')
        lower = request.POST.get('lower')
        o_url = settings.MEDIA_URL + image.split(settings.MEDIA_URL)[1]
        # 剪切图片
        url = cut_image(o_url[1:], int(left), int(upper), int(right), int(lower))
        new_url = url.split('media/')[1]
        return JsonResponse({'code': 200, 'url': settings.MEDIA_URL + new_url})


def download_views(request):
    image_url = request.GET.get('data')
    url = settings.MEDIA_URL + image_url.split(settings.MEDIA_URL)[1]
    title = url.split('/media/images/')[1]

    # # 下载文件
    img = open(url[1:], 'rb')
    response = FileResponse(img)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="' + title + '"'
    return response
