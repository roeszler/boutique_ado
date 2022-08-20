""" Import Modules """
from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.conf import settings

from bag_app.contexts import bag_contents
from .forms import OrderForm


import stripe

# Create your views here.
def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY_BOUTIQUE
    stripe_secret_key = settings.STRIPE_SECRET_KEY_BOUTIQUE

    bag = request.session.get('bag', {})
    if not bag:
        messages.error(request, "There's nothing in your shopping bag at the moment")
        return redirect(reverse('products'))  # prevent people from manually accessing the URL by typing '/checkout'
    
    # Part of the function to calculate the current bag total in the view.
    current_bag = bag_contents(request)
    total = current_bag['grand_total'] # get total from accessing the grand_total key out of the current bag
    stripe_total = round(total * 100) # Since stripe will require the amount to charge as an integer

    # set the stripe secret key
    stripe.api_key = stripe_secret_key
    # to create the stripe payment intent:
    intent = stripe.PaymentIntent.create(
        amount=stripe_total,
        currency=settings.STRIPE_CURRENCY,
    )
    # print(intent)

    order_form = OrderForm()

    if not stripe_public_key:
        messages.warning(
            request, 'Stripe public key is missing. \
            Did you forget to set it in your environment?'
            )


    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }

    return render(request, template, context)
