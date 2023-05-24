from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('chatapi/', include('apichat.urls', namespace='apichat')),

    path('', lambda request: redirect('apichat:chat'), name='root_redirect'),

]
