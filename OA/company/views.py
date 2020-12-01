import hashlib
import json
import random

from django.core.cache import cache
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views import View
from company.models import Company
from user.models import UserProfile
from tools.logging_dec import logging_check, get_company_by_request,c_logging_check
from tools.sms import YunTongXin
from django.conf import settings
from .tasks import send_sms
from c_btoken.views import make_token

def company_register(request):
    return HttpResponse('c_register')


class CompanyView(View):
    def post(self, request):
        json_str = request.body
        json_obj = json.loads(json_str)
        c_name = json_obj['c_name']
        email = json_obj['email']
        password_1 = json_obj['password_1']
        password_2 = json_obj['password_2']
        phone = json_obj['phone']
        sms_num = json_obj['sms_num']
        # 验证码校验
        cache_key = 'sms_%s' % (phone)
        old_code = cache.get(cache_key)
        print('old_code>>>>>>>>>>>>>>>>', old_code)
        if int(sms_num) != old_code:
            result = {'code': 10106, 'error': '验证码错误!'}
            return JsonResponse(result)
        # 企业名检验
        if len(c_name) > 40:
            result = {'code': 10100, 'error': '企业名过长'}
            return JsonResponse(result)
        if not c_name:
            result = {'code': 10101, 'error': '未输入企业名'}
            return JsonResponse(result)
        old_company = Company.objects.filter(c_name=c_name)
        if old_company:
            result = {'code': 10102, 'error': '企业名已注册'}
            return JsonResponse(result)
        # 邮箱检验
        if not email:
            result = {'code': 10105, 'error': '请输入邮箱'}
            return JsonResponse(result)
        # 密码检验
        if not password_1:
            result = {'code': 10103, 'error': '未输密码'}
            return JsonResponse(result)
        if password_1 != password_2:
            result = {'code': 10104, 'error': '两次输入密码不一致'}
            return JsonResponse(result)
        md5 = hashlib.md5()
        md5.update(password_2.encode())
        password_m = md5.hexdigest()
        # 插入数据
        try:
            Company.objects.create(c_name=c_name, email=email, password=password_m, phone=phone)
        except Exception as e:
            result = {'code': 10102, 'error': '企业名已注册'}
            return JsonResponse(result)

        # 签发jwt
        token = make_token(email)
        return JsonResponse({'code': 200, 'email': email, 'data': {'token': token.decode()}})


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

    # # 同步发送
    # x = YunTongXin(settings.SMS_ACCOUNT_ID, settings.SMS_ACCOUNT_TOKEN,
    #                settings.SMS_APP_ID, settings.SMS_TEMPLATE_ID)
    # res = x.run(phone, code)
    # print(res)

    # 异步发送
    send_sms.delay(phone, code)

    return JsonResponse({'code': 200})

@c_logging_check
def users_show(request,email_id):
    print('--user get view in--')
    # 1.先获取企业信息,判断有无这个企业
    print(email_id)
    try:
        company = Company.objects.get(email=email_id)
        # company = Company.objects.create(c_name=c_name, email=email,
        c_name  = company.c_name
        c_id = company.id
    except Exception as e:
        result = {'code': 10305, 'error': 'email_id is error'}
        print('>>>>>>>>>>>>',e,'<<<<<<<<<<<',result)
        return JsonResponse(result)
    visitor_emial = get_company_by_request(request)

    if visitor_emial != email_id:
        result = {'code': 10306, 'error': 'please login'}
        print('>>>>>>>>>>>>',result)
        return JsonResponse(result)
    # employer_users = UserProfile.objects.filter(company=c_id)
    # employer_users = [{'username':'xiaoming','nickname':'还望','email':'xiaoming@auo.com'},
    #                   {'username': 'xiaohong', 'nickname': '妖姬', 'email': 'xiaohong@auo.com'}
    #                   ]
    # res = make_users_res(c_name,employer_users)
    employer_users = UserProfile.objects.filter(company_id=c_id)

    res =make_users_res(c_name, employer_users)

    return JsonResponse(res)

# 员工列表列表的返回值
def make_users_res(c_name,employer_users):
    user_res = []
    i = 1
    for user in employer_users:
        d = {}
        d['id'] = i
        d['username'] = user.username
        d['nickname'] = user.nickname
        d['phone'] = user.phone
        user_res.append(d)
        i+=1
    res = {'code': 200,'c_name':c_name, 'data': {}}
    res['data']['users'] = user_res

    return res

@c_logging_check
def user_delete(request,username):
    #
    print(">>>>>>ssss>>>>>>>",username)
    try:
        user = UserProfile.objects.get(username=username)
        print(">>>>>>>>>>>>>",user)
    except Exception as e:
        result = {'code':10400,'error':'未找到此员工'}
        return JsonResponse(result)

    user.company = None
    user.save()

    return JsonResponse({'code':200})