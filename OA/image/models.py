from django.db import models


# Create your models here.
class Images(models.Model):
    # 标题
    title = models.CharField(max_length=50)
    # MEDIA_URL + images
    image = models.ImageField(upload_to='images')
    # 标记
    sign = models.BooleanField(default=False)
