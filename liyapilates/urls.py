"""liyapilates URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path
from django.shortcuts import redirect, reverse

from clientlist import views


urlpatterns = [
    path('client_list/', views.client_list, name='client_list'),
    path('client/<slug:client_slug>/', views.client_details, name='client_details'),
    path('lesson_list/', views.lesson_list, name='lesson_list'),
    path('lesson/<int:pk>/', views.lesson_details, name='lesson_details'),
    path('lesson/new/', views.new_lesson, name='new_lesson'),
    path('admin/', admin.site.urls),
    path('', lambda request: redirect(reverse(viewname='client_list'), permanent=True), name='home'),
]
