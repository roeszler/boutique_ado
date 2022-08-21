""" Secure webhooks to capture important events """
from django.http import HttpResponse


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
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200
        )

    def handle_payment_intent_payment_failed(self, event):
        """
        Handle listening for the payment_intent.payment_failed webhook from Stripe
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200
        )
