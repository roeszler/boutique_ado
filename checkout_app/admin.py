from django.contrib import admin
from .models import Order, OrderLineItem

# Register your models here.
class OrderAdmin(admin.ModelAdmin):
    """
    Add Order, OrderLineItem models to the admin panel
    """
    readonly_fields = (
        'order_number', 'date', 'delivery_cost',
        'order_total', 'grand_total',
    )
    
    # To specify the order of the fields in the admin interface 
    # which would otherwise be adjusted by django
    fields = (
        'order_number', 'date', 'full_name',
        'email', 'phone_number', 'country',
        'postcode', 'town_or_city', 'street_address1',
        'street_address2', 'county', 'delivery_cost',
        'order_total', 'grand_total',
    )

    # To restrict the columns that show up in the order list to only a few key items.
    list_display = (
        'order_number', 'date', 'full_name',
        'order_total', 'delivery_cost', 'grand_total',
    )

    # Order by date in reverse chronological order
    ordering = ('-date',)
