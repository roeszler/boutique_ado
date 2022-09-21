""" Import Modules """
from django.shortcuts import render, redirect, reverse, get_object_or_404, HttpResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.conf import settings

from bag_app.contexts import bag_contents
from products_app.models import Product
from profiles_app.models import UserProfile
from profiles_app.forms import UserProfileForm

from .forms import OrderForm
from .models import Order, OrderLineItem

import stripe
import json

# Create your views here.

# Before we call the confirm card payment method in the stripe JavaScrip,
# we make a post request to this view and give it the client secret from the payment intent.
# If we split that at the word 'secret' the first part of it will be the payment intent Id,
# so we can store that in a variable called 'pid'.
# Then set up stripe with the secret key so we can modify the payment intent.

@require_POST
def cache_checkout_data(request):
    """
    To capture the POST request from stripe payment intent webhook
    """
    try:
        # split the secret to return the payment Intent ID
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY_BOUTIQUE

        # To set up stripe with the secret key so we can modify the payment intent
        # and add some user metadata:
        stripe.PaymentIntent.modify(pid, metadata={
            'bag': json.dumps(request.session.get('bag', {})),
            'save_info': request.POST.get('save_info'),
            'username': request.user,
        })

        return HttpResponse(status=200)

    # to capture exceptions
    except Exception as e:
        # print("ERROR: ", error)
        messages.error(request, 'Sorry, your payment cannot be \
            processed right now. Please try again later.')
        return HttpResponse(content=e, status=400)


def checkout(request):
    """
    To define the actions of the checkout processes:
    Success, form errors, calculate totals, create line items
    and pass information to the user on errors.
    """
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
            # prevent multiple save events by preventing the first from happening
            order = order_form.save(commit=False)

            # split it to get the payment intent id like we did in the cash check out data view
            pid = request.POST.get('client_secret').split('_secret')[0]
            order.stripe_pid = pid
            order.original_bag = json.dumps(bag)
            order.save()

            # need to iterate through the bag items to create each line item
            for item_id, item_data in bag.items():
                try:
                    product = Product.objects.get(id=item_id)

                    # check if integer for product w/ sizes or not
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
        
        # Attempt to prefill the form with any info the user maintains in their profile
        if request.user.is_authenticated:
            try:
                profile = UserProfile.objects.get(user=request.user)
                order_form = OrderForm(initial={
                    # From user accounts:
                    'full_name': profile.user.get_full_name(),
                    'email': profile.user.email,

                    # From default profile:
                    'phone_number': profile.default_phone_number,
                    'country': profile.default_country,
                    'postcode': profile.default_postcode,
                    'town_or_city': profile.default_town_or_city,
                    'street_address1': profile.default_street_address1,
                    'street_address2': profile.default_street_address2,
                    'county': profile.default_county,
                })
            # If not authenticated, render an empty form:
            except UserProfile.DoesNotExist:
                order_form = OrderForm()
        else:
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


def checkout_success(request, order_number):
    """
    To take the order number and render success page
    indicating to the user that their payment is complete.
    """
    save_info = request.session.get('save_info')

    # get order no and send it back to template view
    order = get_object_or_404(Order, order_number=order_number)

    # Attach order details to specific user profile
    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user=request.user)
        # Attach the user's profile to the order
        order.user_profile = profile
        order.save()

        # Save the user's info
        if save_info:
            profile_data = {
                'default_phone_number': order.phone_number,
                'default_country': order.country,
                'default_postcode': order.postcode,
                'default_town_or_city': order.town_or_city,
                'default_street_address1': order.street_address1,
                'default_street_address2': order.street_address2,
                'default_county': order.county,
            }
            # to create an instance of the user profile form
            user_profile_form = UserProfileForm(profile_data, instance=profile)
            if user_profile_form.is_valid():
                user_profile_form.save()

    # email successful order
    messages.success(request, f'Order successfully processed! \
        Your order number is {order_number}. A confirmation \
        email will be sent to {order.email}.')

    # clear users shopping bag
    if 'bag' in request.session:
        del request.session['bag']

    # set and render the template and context
    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
    }
    return render(request, template, context)
