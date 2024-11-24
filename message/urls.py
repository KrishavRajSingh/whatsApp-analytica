from django.urls import path
from . import views
from django.conf import settings

urlpatterns = [
    # path('', views.getData),
    path('', views.postData),
    path('whatsapp', views.receive_whatsapp_message),
    path('sendMsg', views.send_whatsapp_message)
]