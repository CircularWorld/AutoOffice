import redis
import requests
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views import View
import json
import urllib.request
# Create your views here.
class UsersView(View):
    def __init__(self):
       self.project_reply={
            'word':'''上传Word后对文档修改,也可替换数据批量生成word''',
            'excel':'''对表格数据可视化分析,拆分合并表格''',
            'company':'''用于管理企业所属用户,可查看用户信息,以及移出企业组''',
            'user':'''用户个人信息实现,可对部分信息修改''',
            'picture':'''对图片压缩,裁剪,以及添加水印''',
            'localfile':'''对本地文件,进行批量移动、复制、删除和解压操作''',
        }
    def get(self,request):
        return render(request, 'robot_js/robot.html')
    def post(self,request):
        print('*'*50)
        json_str=request.body
        json_obj=json.loads(json_str)
        talk_words=json_obj
        print(talk_words)
        r = redis.Redis(host='localhost', port=6379, db=0)
        api_url = "http://openapi.tuling123.com/openapi/api/v2"
        name='username'#用户名
        while True:
            if name:
                r.sadd('%s:chat' % name, talk_words)
            # # if talk_words in 'word':
            # if 'word' in talk_words or '文档' in talk_words:
            #     # project_reply = 'word'  # 功能详细信息+url跳转页面
            #     return JsonResponse({'results_text':self.project_reply['word']})
            #     # print('功能详细信息+url跳转页面')
            # # elif talk_words in 'excel':
            # elif 'excel' in talk_words:
            #     project_reply = 'excel'  # 功能详细信息+url跳转页面
            #     return JsonResponse({'results_text':project_reply})
            #
            # elif talk_words in '企业':
            #     project_reply = '企业'  # 功能详细信息+url跳转页面
            #     return JsonResponse({'results_text':project_reply})
            #
            # elif talk_words in '用户':
            #     project_reply = '用户'  # 功能详细信息+url跳转页面
            #     return JsonResponse({'results_text':project_reply})
            #
            # elif talk_words in '图像处理':
            #     project_reply = '图像处理'  # 功能详细信息+url跳转页面
            #     return JsonResponse({'results_text':project_reply})
            #
            # elif talk_words in '本地文档处理':
            #     project_reply = '本地文档处理'  # 功能详细信息+url跳转页面
            #     return JsonResponse({'results_text':project_reply})
            if 'word' in talk_words or '文档' in talk_words:
                return JsonResponse({'results_text':self.project_reply['word']})

            elif 'excel' in talk_words or '表格' in talk_words:

                return JsonResponse({'results_text':self.project_reply['excel']})

            elif '企业' in talk_words:

                return JsonResponse({'results_text':self.project_reply['company']})

            elif '用户'  in talk_words:

                return JsonResponse({'results_text':self.project_reply['user']})

            elif '图像' in talk_words or '图片' in talk_words:

                return JsonResponse({'results_text':self.project_reply['picture']})

            elif '本地' in talk_words or '工具' in talk_words:
                # project_reply = '本地文档处理'  # 功能详细信息+url跳转页面
                return JsonResponse({'results_text':self.project_reply['localfile']})

            req = {
                "perception":
                    {
                        "inputText":
                            {
                                "text": talk_words
                            },

                        "selfInfo":
                            {
                                "location":
                                    {
                                        "city": "深圳",
                                        "province": "广州",
                                        "street": "XXX"
                                    }
                            }
                    },
                "userInfo":
                    {
                        "apiKey": '196204e35e3241a3a4431304e449fe00',
                        "userId": 'username'#此处填写用户名 （str格式）
                    }
            }
            req = json.dumps(req).encode('utf8')
            http_post = urllib.request.Request(api_url, data=req, headers={'content-type': 'application/json'})
            response = urllib.request.urlopen(http_post)
            response_str = response.read().decode('utf8')
            response_dic = json.loads(response_str)
            results_text = response_dic['results'][0]['values']['text']
            print(results_text)

            return JsonResponse({'results_text':results_text})
def index(requset):
    return render(requset,'../templates/index.html')
