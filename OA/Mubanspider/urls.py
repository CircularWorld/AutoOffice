from django.urls import path
from . import views

urlpatterns = [
    # 127.0.0.1:8000/Mubanspider/get_search
    path('get_search',views.get_search),
    #127.0.0.1:8000/Mubanspider/search_muban
    path('search_muban',views.search_muban),
]