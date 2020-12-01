from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views import View
import json
from company.models import Company
import hashlib
import time
import jwt
from django.conf import settings

# error code :10200~10299
# Create your views here.
class TokenView(View):
    def post(self, request):
        json_str = request.body
        json_obj = json.loads(json_str)
        email = json_obj['email']
        password = json_obj['password']
        print('email>>>>>',email)
        print('password>>>>>',password)
        try:
            old_user = Company.objects.get(email=email)
            print('old_user>>>>>',old_user)
        except Exception as e:
            print('error is %s' % e)
            result = {'code':10201,'error':'邮箱或密码错误'}
            return JsonResponse(result)
        md5 = hashlib.md5()
        md5.update(password.encode())
        password_m = md5.hexdigest()
        if password_m != old_user.password:
            result = {'code': 10201, 'error': '邮箱或密码错误'}
            return JsonResponse(result)
        # 签发token
        token = make_token(email)
        return JsonResponse({'code': 200,'email':email,'data':{'token':token.decode()}})

    def get(self, request):
        return HttpResponse('-token get-')

def make_token(email, expire=3600 * 24):
    key = settings.JWT_TOKEN_KEY
    now = time.time()
    payload = {'email': email, 'exp': now + expire}
    return jwt.encode(payload,key,algorithm='HS256')