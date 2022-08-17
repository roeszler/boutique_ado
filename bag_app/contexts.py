from decimal import Decimal  # using the decimal function since this is a financial transaction and using float is susceptible to rounding errors.
from django.conf import settings

def bag_contents(request):
    """
    Does not return a template, rather a dictionary called 'context'
    Known as a context processor, it makes this dictionary available
    to all templates across the entire bag_app application via adding
    it to the TEMPLATES variable in settings.py
    """
    bag_contents = []
    total = 0
    product_count = 0

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
        'bag_contents': bag_contents,
        'total': total,
        'product_count': product_count,
        'delivery': delivery,
        'free_delivery_delta': free_delivery_delta,
        'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
        'grand_total': grand_total,
    }

    return context
