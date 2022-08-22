""" import models """
import uuid  #used to generate the order no.

from django.db import models
from django.db.models import Sum
from django.conf import settings
from django_countries.fields import CountryField

from products_app.models import Product

# when a user checks out:
# First use the information they put into the payment form to create an order instance.
# And iterate through the items in the shopping bag.
# Creating an order line item for each one. Attaching it to the order.
# And updating the delivery cost, order total, and grand total.

class Order(models.Model):
    """ Define the variables that allow us to create and track orders """
    
    order_number = models.CharField(max_length=32, null=False, editable=False) # permanent
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.CharField(max_length=254, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    country = CountryField(blank_label='Country *', null=False, blank=False)
    postcode = models.CharField(max_length=20, null=True, blank=True) # not required in every country
    town_or_city = models.CharField(max_length=40, null=False, blank=False)
    street_address1 = models.CharField(max_length=80, null=False, blank=False)
    street_address2 = models.CharField(max_length=80, null=True, blank=True)
    county = models.CharField(max_length=80, null=True, blank=True) # not required in every country
    date = models.DateTimeField(auto_now_add=True) # automatically set date and time on new orders
    delivery_cost = models.DecimalField(max_digits=6, decimal_places=2, null=False, default=0)
    order_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    original_bag = models.TextField(null=False, blank=False, default='')
    stripe_pid = models.CharField(max_length=254, null=False, blank=False, default='')

    def _generate_order_number(self):
        """ 
        Generate a random, unique order number using UUID.
        underscore indicates that it is a private method which will only
        be used inside this class.
        """
        return uuid.uuid4().hex.upper()  # to generate a random string of 32 numbers we can use as an Order No.

    def update_total(self):
        """
        Update grand total each time the line item is added,
        accounting for delivery costs
        """
        # the last '0' makes sure that on deletion of all lines, the order total to 'zero' instead of none
        self.order_total = self.lineitems.aggregate(Sum('lineitem_total'))['lineitem_total__sum'] or 0
        if self.order_total < settings.FREE_DELIVERY_THRESHOLD:
            self.delivery_cost = self.order_total * settings.STANDARD_DELIVERY_PERCENTAGE / 100
        else:
            self.delivery_cost = 0
        self.grand_total = self.order_total + self.delivery_cost
        self.save()

    def save(self, *args, **kwargs):
        """
        To override the default save method to create the 
        Order No. if it hasn't been set already.
        """
        if not self.order_number:
            self.order_number = self._generate_order_number()
        # execute the original save method
        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_number


class OrderLineItem(models.Model):
    """ controls individual shopping bag items in the Order model """
    order = models.ForeignKey(Order, null=False, blank=False, on_delete=models.CASCADE, related_name='lineitems')
    product = models.ForeignKey(Product, null=False, blank=False, on_delete=models.CASCADE)
    product_size = models.CharField(max_length=2, null=True, blank=True) # XS, S, M, L, XL
    quantity = models.IntegerField(null=False, blank=False, default=0)
    lineitem_total = models.DecimalField(max_digits=6, decimal_places=2, null=False, blank=False, editable=False)

    def save(self, *args, **kwargs):
        """
        To override the default save method to set the lineitem total 
        and update the order total
        """
        self.lineitem_total = self.product.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f'SKU {self.product.sku} on order {self.order.order_number}'
