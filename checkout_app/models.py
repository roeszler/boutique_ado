""" import models """
import uuid #used to generate the order no.

from django.db import models
from django.db.models import Sum
from django.conf import settings

from products_app.model import Product


class Order(models.Model):
    """ Define the variables that allow us to create and track orders """
    order_number = models.CharField(max_length=32, null=False, editable=False) # permanent
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.CharField(max_length=254, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    country_code = models.CharField(max_length=40, null=False, blank=False)
    postcode = models.CharField(max_length=20, null=True, blank=True) # not required in every country
    town_or_city = models.CharField(max_length=40, null=False, blank=False)
    street_address1 = models.CharField(max_length=80, null=False, blank=False)
    street_address2 = models.CharField(max_length=80, null=True, blank=True)
    county = models.CharField(max_length=80, null=True, blank=True) # not required in every country
    date = models.DateTimeField(auto_now_add=True) # automatically set date and time on new orders
    delivery_cost = models.DecimalField(max_digits=6, decimal_places=2, null=False, default=0)
    order_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)


# when a user checks out:
# First use the information they put into the payment form to create an order instance.
# And iterate through the items in the shopping bag.
# Creating an order line item for each one. Attaching it to the order.
# And updating the delivery cost, order total, and grand total.

class OrderLineItem(models.Model):
    """ controls individual shopping bag items in the Order model """
    order = models.ForeignKey(Order, null=False, blank=False, on_delete=models.CASCADE, related_name='lineitems')
    product = models.ForeignKey(Product, null=False, blank=False, on_delete=models.CASCADE)
    product_size = models.CharField(max_length=2, null=True, blank=True) # XS, S, M, L, XL
    quantity = models.IntegerField(null=False, blank=False, default=0)
    lineitem_total = models.DecimalField(max_digits=6, decimal_places=2, null=False, blank=False, editable=False)
