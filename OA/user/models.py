from django.db import models
from company.models import Company

# Create your models here.
class UserProfile(models.Model):
    username = models.CharField("用户名", max_length=11, primary_key=True)
    nickname = models.CharField("昵称", max_length=50)
    phone = models.CharField("手机", max_length=11, default='')
    password = models.CharField("密码", max_length=32)
    avatar = models.ImageField("头像", upload_to='avatar', null=True)
    # collection = models.CharField("收藏", max_length=200, default='')
    # email = models.EmailField("邮箱")
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)


class Meta:
    db_table = 'user_user_profile'
