from django.urls import path
from . import views

app_name = 'chatapi'

urlpatterns = [
    path('command/', views.command, name='command'),
    path('response/', views.response, name='response'),

    path('get_response/', views.get_response, name='get_response'),
    path('set_command/', views.set_command, name='set_command'),

    path('update/', views.update_chat_message, name='update_chat_message'),

    path('', views.chat, name='chat'),
]
