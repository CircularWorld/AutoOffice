"""
图片工具
"""
import time

from PIL import Image
import os
import cv2


def get_outfile(infile: str):
    dir, suffix = os.path.splitext(infile)
    dir_list = dir.split('x-x')
    t = int(time.time() * 1000)
    # if len(dir_list) == 1:
    #     outfile = '{}x-x{}{}'.format(dir_list[0], t, suffix)
    # else:
    outfile = '{}x-x{}{}'.format(dir_list[0], t, suffix)

    return outfile


def cut_image(infile, left, upper, right, lower):
    """
    剪切图片函数
    :param title:标题
    :param infile:图片路径
    :param left:左坐标（x1）
    :param upper:上坐标（y1）
    :param right:右坐标（x2）
    :param lower:下坐标（y2）
    :return:图片标题，修改后图片地址
    """
    img = Image.open(infile)
    cropped1 = img.crop((left, upper, right, lower))  # (left, upper, right, lower)
    url = get_outfile(infile)
    cropped1.save(url)
    return url


def compress_image(infile, ratio=1):
    """修改图片尺寸
    :param infile: 图片源
    :param outfile: 重设尺寸文件保存地址
    :param x_s: 设置的宽度
    :return:图片标题，修改后图片地址
    """
    im = Image.open(infile)
    x, y = im.size
    x_s = int(x * ratio)
    y_s = int(y * ratio)
    out = im.resize((x_s, y_s), Image.ANTIALIAS)
    print("11111111111", infile)
    url = get_outfile(infile)
    print("11111111111", url)
    out.save(url)
    # new_url = url.split('media/')[1]
    return url


def add_water(image, content, x=100, y=100, size=10):
    """
    添加 水印
    :param image: 图片路径
    :param content: 水印文字
    :param title: 图片标题
    :param size: 大小
    :return:标题+地址
    """

    # 载入
    img = cv2.imread(image)
    # 给水印添加文字(图片、文字、位置、字体、大小、颜色、粗细)
    img2 = cv2.putText(img, content, (x, y), cv2.LINE_4, size, (249, 249, 249), 4)
    # 路径重置
    # new_title = get_outfile(title)
    url = get_outfile(image)
    # 保存图片
    cv2.imwrite(url, img2)
    # new_url = url.split('media/')[1]
    return url
