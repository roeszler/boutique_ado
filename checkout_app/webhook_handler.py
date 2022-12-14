""" Secure webhooks to capture important events """
from django.http import HttpResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

from .models import Order, OrderLineItem
from products_app.models import Product
from profiles_app.models import UserProfile

import json
import time

class StripeWH_Handler:
    """ Handles Stripe Webhooks """
    
    def __init__(self, request):
        """
        The __init__ method sets up a method that's called every time
        an instance of the class is created.
        to assign the request as an attribute of the class just in case 
        we need to access any attributes of the request coming from stripe.
        """
        self.request = request
    
    def _send_confirmation_email(self, order):
        """Send the user a confirmation email"""
        cust_email = order.email
        
        # To render the conformation emails templates + context to render:
        subject = render_to_string(
            'checkout/confirmation_emails/confirmation_email_subject.txt',
            {'order': order})
        # message body
        body = render_to_string(
            'checkout/confirmation_emails/confirmation_email_body.txt',
            {'order': order, 'contact_email': settings.DEFAULT_FROM_EMAIL})
        
        # To send the email
        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            # list of emails to send to:
            [cust_email]
        )
    
    def handle_event(self, event):
        """
        Handle that listens for a generic/unknown/unexpected webhook event
        """
        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}',
            status=200
        )
    
    def handle_payment_intent_succeeded(self, event):
        """
        Handle listening for the payment_intent.succeeded webhook from Stripe
        """

        # to ensure that all orders are entered into our database even in the event 
        # of a user error during the checkout process:
        intent = event.data.object
        pid = intent.id
        bag = intent.metadata.bag
        save_info = intent.metadata.save_info

        billing_details = intent.charges.data[0].billing_details
        shipping_details = intent.shipping
        grand_total = round(intent.charges.data[0].amount / 100, 2)

        # To ensure the data is in the same form as what we want in our database:
        # Clean data in the shipping details
        for field, value in shipping_details.address.items():
            if value == "":
                shipping_details.address[field] = None
        
        # Update profile information if save_info was checked
        profile = None  # can still allow anonymous users to checkout
        username = intent.metadata.username
        # If they are not an anonymoous user, they are authenticated
        if username != 'AnonymousUser':
            # Alternative to request.user...
            profile = UserProfile.objects.get(user__username=username)
            
            # if save info checkbox selected, update defaults:
            if save_info:
                profile.default_phone_number = shipping_details.phone
                profile.default_country = shipping_details.address.country
                profile.default_postcode = shipping_details.address.postal_code
                profile.default_town_or_city = shipping_details.address.city
                profile.default_street_address1 = shipping_details.address.line1
                profile.default_street_address2 = shipping_details.address.line2
                profile.default_county = shipping_details.address.state
                profile.save()
        
        order_exists = False

        # To create a delay to help handle asynchronous processes to line up and 
        # avoid duplicate orders being created:
        attempt = 1
        while attempt <= 5:
            # to get the order using all the information from the payment intent
            # with iexact match that is case insensitive:
            try:
                order = Order.objects.get(
                    full_name__iexact=shipping_details.name,
                    email__iexact=billing_details.email,
                    phone_number__iexact=shipping_details.phone,
                    country__iexact=shipping_details.address.country,
                    postcode__iexact=shipping_details.address.postal_code,
                    town_or_city__iexact=shipping_details.address.city,
                    street_address1__iexact=shipping_details.address.line1,
                    street_address2__iexact=shipping_details.address.line2,
                    county__iexact=shipping_details.address.state,
                    grand_total=grand_total,
                    original_bag=bag,
                    stripe_pid=pid,
                )
                # if the order is found, break out of while loop:
                order_exists = True
                break

            # To create a 5 x 1sec delay to help handle asynchronous processes
            # to line up and avoid duplicate orders being created. Increment
            # attempt by 1 and use .time module to .sleep for one second:
            except Order.DoesNotExsist:
                attempt += 1
                time.sleep(1)
        
        if order_exists:
            # Payment completed, so definitely send an email:
            self._send_confirmation_email(order)

            # Our 200 response
            return HttpResponse(
                content=f'Webhook received: {event["type"]} | SUCCESS: Verified order already in database',
                status=200)
        else:
            order = None
            try:
                order = Order.objects.create(
                    full_name=shipping_details.name,
                    user_profile=profile,
                    email=billing_details.email,
                    phone_number=shipping_details.phone,
                    country=shipping_details.address.country,
                    postcode=shipping_details.address.postal_code,
                    town_or_city=shipping_details.address.city,
                    street_address1=shipping_details.address.line1,
                    street_address2=shipping_details.address.line2,
                    county=shipping_details.address.state,
                    original_bag=bag,
                    stripe_pid=pid,
                )
                # To load the bag from the JSON version in the payment intent
                # instead of from the session:
                for item_id, item_data in json.loads(bag).items():
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

            # if anything goes wrong; delete the order if it was created, and
            # return a 500 server error response to stripe.
            # This will cause stripe to automatically try the webhook again later:
            except Exception as e:
                if order:
                    order.delete()
                return HttpResponse(
                    content=f'Webhook received: {event["type"]} | ERROR: {e}',
                    status=500)

        # if order created by webhook handler:
        self._send_confirmation_email(order)
        
        return HttpResponse(
            content=f'Webhook received: {event["type"]} | SUCCESS: Created order in webhook',
            status=200)

    def handle_payment_intent_payment_failed(self, event):
        """
        Handle listening for the payment_intent.payment_failed webhook from Stripe
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200
        )
