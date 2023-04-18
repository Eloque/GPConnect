from django.urls import path
from . import views

app_name = 'chatapi'

urlpatterns = [
    path('input/', views.input, name='input'),
    path('output/', views.output, name='output'),
    path('command/', views.command, name='command'),
    path('response/', views.response, name='response'),

    path('chat/', views.chat, name='chat'),
    path('update/', views.update_chat_message, name='update_chat_message'),
]
