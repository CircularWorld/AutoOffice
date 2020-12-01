from django.urls import path

from company import views

urlpatterns = [
    # 127.0.0.1:8000/v1/companys/register
    path('register/',views.company_register),
    path('sms',views.sms_view),
    # 127.0.0.1:8000/v1/companys/users_show
    path('users_show/<str:email_id>',views.users_show),
    # 127.0.0.1:8000/v1/companys/user_delete/小工
    path('user_delete/<str:username>',views.user_delete),

]
