""" import modules """
from decimal import Decimal  # using the decimal function since this is a financial transaction and using float is susceptible to rounding errors.
from django.conf import settings
from django.shortcuts import get_object_or_404
from products_app.models import Product

def bag_contents(request):
    """
    Does not return a template, rather a dictionary called 'context'
    Known as a context processor, it makes this dictionary available
    to all templates across the entire bag_app application via adding
    it to the TEMPLATES variable in settings.py
    """
    bag_items = []
    total = 0
    product_count = 0
    bag = request.session.get('bag', {})  # get it if it exists, empty dictionary if not

    # to iterate the shopping bag, tally up the total cost and product count and 
    # add the products and their data to the bag items list:
    for item_id, item_data in bag.items():  # nb: in the bag from the 'session'!

        # To only execute code if item has no sizes, check if item_data is an integer
        if isinstance(item_data, int):
            product = get_object_or_404(Product, pk=item_id)  # get the product
            total += item_data * product.price  # add calc to add to total
            product_count += item_data  # increase product count by quantity

            # add a dictionary to the list of bag items containing not only the id and the quantity,
            # but also the product object itself, allowing access to product items when iterating
            # through bag items in our templates
            bag_items.append({
                'item_id': item_id,
                'quantity': item_data,
                'product': product,
            })
        else:
            product = get_object_or_404(Product, pk=item_id)  # get the product

            # the item is a dictionary (not an integer) and needs to iterate through
            # inner dictionary, return no. of items and increment the product count and totals
            # then render the size to the template
            for size, quantity in item_data['items_by_size'].items():
                total += quantity * product.price
                product_count += quantity
                bag_items.append({
                'item_id': item_id,
                'quantity': quantity,
                'product': product,
                'size': size,
            })


    if total < settings.FREE_DELIVERY_THRESHOLD:
        delivery = total * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE / 100)
        # lets user know how much more they need to spend to get free delivery
        free_delivery_delta = settings.FREE_DELIVERY_THRESHOLD - total
    else:
        # If the total is greater than or equal to the threshold
        delivery = 0
        free_delivery_delta = 0
    
    grand_total = delivery + total

    # add to context so they will be available to templates across the project
    context = {
        'bag_items': bag_items,
        'total': total,
        'product_count': product_count,
        'delivery': delivery,
        'free_delivery_delta': free_delivery_delta,
        'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
        'grand_total': grand_total,
    }

    return context
