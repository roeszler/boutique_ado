# from django.contrib import admin
from django.urls import path
# import views from the current directory
from . import views

urlpatterns = [
    path('', views.view_bag, name='view_bag'),
]
