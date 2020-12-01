from django.urls import path,re_path
from . import views,data_views

urlpatterns = [
    # 数据可视化路由
    # path('data_visualization',views.data_visualization),
    path('data_visualization',data_views.data_visualization),
    re_path('download', data_views.file_response_download),
    # excel 上传
    path('upload_excel',views.upload_excel),
    path('upload_zip',views.upload_zip),
    # excel 拆分
    path('split',views.split),
    path('merge',views.mergetable),
]