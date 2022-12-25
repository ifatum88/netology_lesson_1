"""api_with_restrictions URL Configuration

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

# from rest_framework.routers import DefaultRouter

from advertisements.views import main_page, AdvertisementViewSet

# Реализация маршрутов переехала в advertisements.views
urlpatterns = [
    path('', main_page, name="main"),
    path('api/', include('advertisements.urls'), name="api"),
    path('admin/', admin.site.urls, name="admin"),
]