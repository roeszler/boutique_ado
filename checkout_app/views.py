""" Import Modules """
from django.shortcuts import render, redirect, reverse
from django.contrib import messages

from .forms import OrderForm
from bag_app.contexts import bag_contents

# Create your views here.
def checkout(request):
    bag = request.session.get('bag', {})
    if not bag:
        """ if nothing in the bag """
        messages.error(request, "There's nothing in your shopping bag at the moment")
        return redirect(reverse('products'))  # prevent people from manually accessing the URL by typing '/checkout'
    
    # Part of the function to calculate the current bag total in the view.
    current_bag = bag_contents(request)
    total = current_bag['grand_total'] # get total from accessing the grand_total key out of the current bag
    stripe_total = round(total * 100) # Since stripe will require the amount to charge as an integer.

    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': 'pk_test_51LYTPcLAd9Hb7YyJuL2gamYTYu1q08RDghS35m9nFmBsEMgYAZ19gPuOY4kaz1orFM0R5szUds1qpGEoHWmzIxTX00B0UEPHUi',
        'client_secret': 'test client secret',
    }

    return render(request, template, context)