import json

import requests
from django.http import JsonResponse
from django.shortcuts import render
from urllib import parse
from fake_useragent import UserAgent
import random
from lxml import etree

# Create your views here.
def get_search(request):
    return render(request,'Mubanspider/search_muban.html')


def search_muban(request):
    # json 字符串
    json_str = request.body
    json_obj = json.loads(json_str)
    word = json_obj['keyword']

    print('>>>>>',word)

    result=parse.quote(word)
    # 拼接ｕrl地址，获取该页面的响应内容
    one_url = 'https://www.glzy8.com/search.html?keyword={}'.format(result)
    headers={'User-Agent':UserAgent().random}
    # import requests
    html=requests.get(url=one_url,headers=headers).content.decode('utf-8','ignore')
    # print(html)
    # 一级界面解析
    p = etree.HTML(html)
    ob = p.xpath('//ul[@class="list1"]')[0]
    # 匹配一级界面ｕｒｌ
    url_list = ob.xpath('li/div/a[@class="img"]/@href')
    # 匹配模板图片ｕｒｌ
    img_list = ob.xpath('li/div/a[@class="img"]/img/@src')
    # 匹配模板名
    name_list = ob.xpath('li/div/a[@class="bt"]/text()')
    # 匹配二级界面模板真实下载地址
    downld_url_list=[]
    for url in url_list:
        two_url='https://www.glzy8.com'+url
        html=requests.get(url=two_url,headers=headers).content.decode('utf-8','ignore')
        p1=etree.HTML(html)
        oj=p1.xpath('//div[@class="lis"]')[1]
        # 模板下载地址
        downld_url='https://www.glzy8.com'+oj.xpath('a[contains(@onclick,"addVisit")]/@href')[0]
        downld_url_list.append(downld_url)
    json_data=[]
    for i in range(0,len(url_list)):
        json_dict={}
        json_dict['img_url']=img_list[i]
        json_dict['muban_name']=name_list[i]
        json_dict['download_url']=downld_url_list[i]
        json_data.append(json_dict)
    #print(json_data)
    res={'code':200,'data':{'muban_info':json_data}}
    return JsonResponse(res)























