from django.urls import path
from . import views
urlpatterns = [
    #
    path('robot',views.UsersView.as_view()),
    # path('index',views.index)
]