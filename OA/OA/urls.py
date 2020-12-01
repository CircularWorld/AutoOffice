"""OA URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from company import views as company_views
from c_btoken import views as c_btoken_views
from OAtoken import views as OAtoken_views
from word import views as word_view
from user import views as user_views
urlpatterns = [
    path('admin/', admin.site.urls),
    # 企业模块
    path('v1/companys',company_views.CompanyView.as_view() ),
    path('v1/companys/', include('company.urls')),
    path('v1/c_tokens', c_btoken_views.TokenView.as_view()),
    # 用户模块
    path('v1/users',user_views.UsersView.as_view()),
    path('v1/users/',include('user.urls')),
    path('v1/tokens',OAtoken_views.TokenView.as_view()),
    # excel 数据分析  表格拆分合并
    path('excel/',include('excel.urls')),
    # 表格拆分合并
    path('v1/excels/',include('excel.urls')),
    # 本地工具下载
    path(r'v1/downloads/',include('download.urls')),
    # 模板搜索
    path(r'Mubanspider/',include('Mubanspider.urls')),
    # 图形处理
	path('v1/images/', include('image.urls')),
    # word 文档处理
	path('v1/words/', include('word.urls')),
    # 智能机器人
    path('robot/', include('robot_js.urls')),

]

urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)