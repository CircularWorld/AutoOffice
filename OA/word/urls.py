from django.conf.urls.static import static
from django.urls import path
from django.conf import settings

from word import views

urlpatterns = [

                  path('', views.word_view),

                  path('upload', views.upload_view),

                  path('modify', views.modify_view),

                  path('batch', views.batch_view),

                  path('download', views.download_view),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
