from django.db import models


# Create your models here.
class Words(models.Model):
    # 标题
    title = models.CharField(max_length=50)
    # MEDIA_URL + images
    file = models.ImageField(upload_to='file')
