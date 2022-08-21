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
        """ Handle a generic/unknown/unexpected webhook event """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200
        )
