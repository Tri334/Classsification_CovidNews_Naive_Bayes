from django.urls import path
from . import models
from . import views

urlpatterns = [
    path('', views.home, name='homes'),
    path('admin_page/', views.admin, name='add_data'),
    path('off/', views.dumpData, name='dump'),
    path('sendjson/', views.send_json, name='send_json'),
]
