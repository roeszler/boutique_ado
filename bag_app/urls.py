""" import modules """
from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_bag, name='view_bag'),
    path('add/<item_id>/', views.add_to_bag, name='add_to_bag'), # add_to_bag function in views.py
    path('adjust/<item_id>/', views.adjust_bag, name='adjust_bag'), # adjust_bag function in views.py
    path('remove/<item_id>/', views.remove_from_bag, name='remove_from_bag'), # remove_from_bag function in views.py
]