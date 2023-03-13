"""weekly_reports URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.conf.urls import url

from reports.views import home, other_list_view, vul_list_view, mal_list_view, download_other, download_vul, download_mal, extract, OtherAPIView, MalAPIView, VulAPIView, SearchAPIView

urlpatterns = [
    path('', home, name = 'home'),
    path('admin/', admin.site.urls),
    path('other/', other_list_view, name = 'other'),
    path('upload/other.txt', download_other, name = 'down_other'),
    path('vul/', vul_list_view, name = 'vul'),
    path('upload/vul.txt', download_vul, name = 'down_vul'),
    path('mal/', mal_list_view, name = 'mal'),
    path('upload/mal.txt', download_mal, name = 'down_mal'),
    path('upload/csv.zip', extract, name = 'extract'),
    path('accounts/', include('django.contrib.auth.urls')),
    url('api/other/', OtherAPIView.as_view()),
    url('api/mal/', MalAPIView.as_view()),
    url('api/vul/', VulAPIView.as_view()),
    url('api/search/', SearchAPIView.as_view())
]