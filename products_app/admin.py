from django.contrib import admin
from .models import Product, Category

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    """ to extend the built in model admin class: product list view """
    list_display = (
        'sku',
        'name',
        'category',
        'price',
        'rating',
        'image',
    )

    # tuple to sort the products by SKU using the ordering attribute
    ordering = ('sku', )

class CategoryAdmin(admin.ModelAdmin):
    """ to extend the built in model admin class: category list view """
    list_display = (
        'friendly_name',
        'name',
    )



admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
