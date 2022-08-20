""" Import Modules """
from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.conf import settings

from bag_app.contexts import bag_contents
from products_app.models import Product

from .forms import OrderForm
from .models import OrderLineItem


import stripe

# Create your views here.
def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY_BOUTIQUE
    stripe_secret_key = settings.STRIPE_SECRET_KEY_BOUTIQUE

    # handle a successful payament
    if request.method == 'POST':
        bag = request.session.get('bag', {})

        form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'country': request.POST['country'],
            'postcode': request.POST['postcode'],
            'town_or_city': request.POST['town_or_city'],
            'street_address1': request.POST['street_address1'],
            'street_address2': request.POST['street_address2'],
            'county': request.POST['county'],
        }
        order_form = OrderForm(form_data)
        if order_form.is_valid():
            order = order_form.save()

            # need to iterate through the bag items to create each line item
            for item_id, item_data in bag.items():
                try:
                    product = Product.objects.get(id=item_id)

                    # check if intieger for product w/ sizes or not
                    if isinstance(item_data, int):
                        order_line_item = OrderLineItem(
                            order=order,
                            product=product,
                            quantity=item_data,
                        )
                        order_line_item.save()
                    else:
                        # product with sizes, iterate through and create line item accordingly
                        for size, quantity in item_data['items_by_size'].items():
                            order_line_item = OrderLineItem(
                                order=order,
                                product=product,
                                quantity=quantity,
                                product_size=size,
                            )
                            order_line_item.save()

                # if product is not found; error, delete, return to shopping bag
                except Product.DoesNotExist:
                    messages.error(request, (
                        "One of the products in your bag wasn't found in our database. "
                        "Please call us for assistance!")
                    )
                    order.delete()
                    return redirect(reverse('view_bag'))
            
            # check if user wanted to save their information and redirect to checkout_success
            request.session['save_info'] = 'save-info' in request.POST
            return redirect(reverse('checkout_success', args=[order.order_number]))
        else:
            messages.error(request, 'There was an error with your form. \
                Please double check your information.')

    else:
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
