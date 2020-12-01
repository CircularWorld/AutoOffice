from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views import View
import json

from company.models import Company
from .models import UserProfile
import hashlib
from OAtoken.views import make_token
from django.conf import settings
import time
import jwt
from tools.logging_dec import logging_check
from django.utils.decorators import method_decorator
from django.core.cache import cache
import random
from tools.sms import YunTongXin
from django.conf import settings
from .tasks import send_sms

# from .tasks import send_sms

# Create your views here.

# user的code: 10100~10199
class UsersView(View):
    def get(self, request, username=None):
        if username:
            try:
                user = UserProfile.objects.get(username=username)
            except Exception as e:
                print("get user error %s" % e)
                result = {'code': 10104, 'error': '用户名错误'}
                return JsonResponse(result)
            # 根据查询字符串的键获取指定的数据
            if request.GET.keys():
                data = {}
                for k in request.GET.keys():
                    if k == 'password':
                        continue
                    if hasattr(user, k):
                        data[k] = getattr(user, k)
                result = {'code': 200, 'username': username, 'data': data}
                return JsonResponse(result)
            else:
                try:
                    companyname = user.company.c_name
                except Exception as e:
                    print(username,'没有选择公司')
                    companyname= ''

                result = {'code': 200, 'username': username,
                          'data': {
                                   'nickname': user.nickname, 'avatar': str(user.avatar),
                          'companyname': companyname}}
                return JsonResponse(result)
        else:
            return HttpResponse('-all users-')

    def post(self, request):
        json_str = request.body
        json_obj = json.loads(json_str)
        username = json_obj['username']
        nickname = json_obj['nickname']
        phone = json_obj['phone']
        password_1 = json_obj['password_1']
        password_2 = json_obj['password_2']
        sms_num = json_obj['sms_num']
        # 校验验证码
        cache_key = 'sms_%s' % (phone)
        old_code = cache.get(cache_key)
        # 验证码过期
        if not old_code:
            result = {'code': 10113, 'error': '验证码过期,请重新发送验证码'}
            return JsonResponse(result)
        # 比较
        if int(sms_num) != old_code:
            result = {'code': 10114, 'error': '验证码有误,请重新输入'}
            return JsonResponse(result)

        if len(username) > 11:
            result = {'code': 10100, 'error': '用户名大于11位,请重新输入'}
            return JsonResponse(result)
        # 用户名是否可用
        old_user = UserProfile.objects.filter(username=username)
        if old_user:
            result = {'code': 10101, 'error': '用户名已存在,请重新输入'}
            return JsonResponse(result)
        # 处理密码
        if password_1 != password_2:
            result = {'code': 10102, 'error': '密码错误,请确认后重新输入'}
            return JsonResponse(result)
        md5 = hashlib.md5()
        md5.update(password_1.encode())
        password_m = md5.hexdigest()
        # 插入数据
        try:
            user = UserProfile.objects.create(username=username,
                                              password=password_m, nickname=nickname,
                                              phone=phone,)
        except Exception as e:
            print('create error is %s' % e)
            result = {'code': 10101, 'error': '用户名已存在,请重新输入'}
            return JsonResponse(result)

        # 签发jwt
        token = make_token(username)
        return JsonResponse({'code': 200, 'username': username, 'data': {'token': token.decode()}})

    @method_decorator(logging_check)
    def put(self, request, username):
        # user从装饰器中给request增加的附加属性myuser获取
        json_str = request.body
        json_obj = json.loads(json_str)

        request.myuser.nickname = json_obj["nickname"]
        companyname = json_obj["companyname"]
        print('companyname:>>>>>',companyname)
        if not companyname:
            request.myuser.company = None
            companyname = ''
        else:
            try:
                company = Company.objects.get(c_name = companyname)
                print('企业ID', company.id)
                request.myuser.company = company
                companyname = request.myuser.company.c_name
            except Exception as e:
                result = {'code':10103,'error':'企业名未找到,请确认该企业是否注册'}
                return JsonResponse(result)

        # print('myuser.company:>>>>>',request.myuser.company)

        request.myuser.save()
        result = {'code': 200, 'username': request.myuser.username,'companyname': companyname}
        return JsonResponse(result)


@logging_check
def user_avatar(request,username):
    if request.method != 'POST':
        result = {'code': 10105, 'error': '请提交数据'}
        return JsonResponse(result)
    # 1.从url中获取username
    # user = UserProfile.objects.get(username=username)

    # 2.从装饰器中由request的附加属性myuser获取user
    user = request.myuser
    user.avatar = request.FILES['avatar']
    user.save()

    result = {'code': 200, 'username': user.username}
    return JsonResponse(result)

@logging_check
def user_password(request,username):
    if request.method !='POST':
        result = {'code':202,'error':'请提交数据'}
        return JsonResponse(result)
    if request.method == 'POST':
        json_str = request.body
        json_obj = json.loads(json_str)

        #输入框获取旧密码
        old_password = json_obj['old_password']
        password_1 = json_obj['password_1']
        password_2 = json_obj['password_2']
        # print(old_password)
        # print(password_1)
        # print(password_2)
        #获取数据库的加密密码
        sq_password = UserProfile.objects.get(username=username).password
        print(sq_password)
        #输入框的旧密码加密
        md5 = hashlib.md5()
        md5.update(old_password.encode())
        password_m = md5.hexdigest()
        print(password_m)
        if old_password == '':
            result = {'code':202,'error':'旧密码不能为空'}
            return JsonResponse(result)
        elif password_1 == '':
            result = {'code':202,'error':'新密码不能为空'}
            return JsonResponse(result)
        elif password_2 == '':
            result = {'code':202,'error':'再次密码不能为空'}
            return JsonResponse(result)
        elif old_password == password_1:
            result = {'code': 202, 'error': '新旧密码不能相同'}
            return JsonResponse(result)

        #于数据库旧密码比对
        if sq_password != password_m:
            result = {'code':206,'error':'旧密码输入不正确'}
            return JsonResponse(result)
        else:
            #输入的两次密码进行比较
            if password_1 != password_2:
                result = {'code':206,'error':'两次密码不一致'}
                return JsonResponse(result)
            #新密码加密
            md5 = hashlib.md5()
            md5.update(password_2.encode())
            new_password_md5 = md5.hexdigest()
            print(new_password_md5)
            #修改数据库中密码

            user = UserProfile.objects.get(username=username)
            user.password = new_password_md5
            user.save()
            result = {'code': 200}
            return JsonResponse(result)

def sms_view(request):
    json_str = request.body
    json_obj = json.loads(json_str)
    phone = json_obj['phone']
    print(phone)
    # 防止用户多次点击按钮重复发送验证码
    cache_key = 'sms_%s' % (phone)
    old_code = cache.get(cache_key)
    if old_code:
        result = {'code': 10112, 'error': '请稍后再来'}
        return JsonResponse(result)
    # 生成随机码
    code = random.randint(1000, 9999)
    print(code)
    # 放到缓存中,有效期65秒
    cache.set(cache_key, code, 65)
    send_sms.delay(phone,code)
    return JsonResponse({'code': 200})
