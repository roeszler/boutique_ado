# from django.contrib import admin
from django.urls import path
# import views from the current directory
from . import views

urlpatterns = [
    path('', views.all_products, name='products'),

    # django will always use the first URL it finds a matching pattern for.
    # In this case unless we specify that product_id is an integer django 
    # doesn't know the difference between a product number and a string: 
    path('<int:product_id>/', views.product_detail, name='product_detail'), # 'int:' creates it as an integer
    path('add/', views.add_product, name='add_product'),
    path('edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path('delete/<int:product_id>/', views.delete_product, name='delete_product'),
]
