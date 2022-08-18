from django import template

# to register the custom filter
register = template.Library()

# register filter decorator to register our function as a template filter:
@register.filter(name='calc_subtotal')
def calc_subtotal(price, quantity):
    return price * quantity