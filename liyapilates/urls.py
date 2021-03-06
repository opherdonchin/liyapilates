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

#  TODO: Add login and users
urlpatterns = [
    path('client_list/', views.client_list, name='client_list'),
    path('new_client/', views.new_client, name='new_client'),
    path('client/<slug:client_slug>/', views.client_details, name='client_details'),
    path('client/<slug:client_slug>/edit/', views.edit_client, name='edit_client'),  # TODO: make edit_client view
    path('client/<slug:client_slug>/new_card/', views.add_card, name='add_card'),
    path('client/<slug:client_slug>/edit_card/<int:card_pk>/', views.edit_card, name='edit_card'),
    path('client/<slug:client_slug>/cards/', views.ClientCards.as_view(), name='client_cards'),
    path('client/<slug:client_slug>/lessons/', views.client_lessons, name='client_lessons'),
    path('lesson_list/', views.lesson_list, name='lesson_list'),
    path('lesson/<int:pk>/', views.lesson_details, name='lesson_details'),
    path('lesson/<int:pk>/edit/', views.edit_lesson, name='edit_lesson'),
    path('new_lesson/', views.new_lesson, name='new_lesson'),
    path('admin/', admin.site.urls),
    path('', lambda request: redirect(reverse(viewname='client_list'), permanent=True), name='home'),
]
