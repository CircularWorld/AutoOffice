from django.urls import path

from download import views

urlpatterns = [
    path('test', views.test),
    # 'user_delete/<str:username>'
    path(r'zip/<str:filename>', views.user_zip_download),
    path(r'excel/upload_zipfile/<str:filename>', views.user_excel_download),
    # http://127.0.0.1:8000/v1/downloads/localtool
    path(r'localtool', views.localtool_download),

]
