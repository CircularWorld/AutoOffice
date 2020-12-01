from django.conf.urls.static import static
from django.urls import path
from django.conf import settings
from image import views

urlpatterns = [
                  path('img', views.image_views),

                  # 上传
                  path('img/upload', views.upload_views),

                  # 添加水印
                  path('img/water', views.water_views),

                  # 压缩
                  path('img/compress', views.compress_views),

                  # 剪切
                  path('img/cut', views.cut_views),

                  # 下载
                  path('img/download', views.download_views),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
