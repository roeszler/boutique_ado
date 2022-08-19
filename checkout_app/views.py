""" Import Modules """
from django.shortcuts import render, redirect, reverse
from django.contrib import messages

from .forms import OrderForm

# Create your views here.
def checkout(request):
    bag = request.session.get('bag', {})
    if not bag:
        """ if nothing in the bag """
        messages.error(request, "There's nothing in your shopping bag at the moment")
        return redirect(reverse('products'))  # prevent people from manually accessing the URL by typing '/checkout'
    
    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
    }

    return render(request, template, context)