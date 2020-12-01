from django.db import models

# Create your models here.
class Company(models.Model):
    c_name = models.CharField('企业名',max_length=40,unique=True)
    email = models.EmailField('企业邮箱',default='',unique=True)
    password = models.CharField('密码',max_length=32)
    phone = models.CharField("手机", max_length=11, default='')
    create_time = models.DateTimeField('创建时间',auto_now_add=True)
    update_time = models.DateTimeField('更新时间',auto_now=True)


# Create your models here.
#class UserProfile(models.Model):
#    username = models.CharField("用户名", max_length=11, primary_key=True)
#    nickname = models.CharField("昵称", max_length=50)
#    email = models.EmailField("邮箱")
#    password = models.CharField("密码", max_length=32)
#    avatar = models.ImageField("头像", upload_to='avatar', null=True)
#    phone = models.CharField("手机", max_length=11, default='')
#    collection = models.CharField('收藏',max_length=200)
#    company = models.ForeignKey(Company,on_delete=models.SET_NULL,null=True)

