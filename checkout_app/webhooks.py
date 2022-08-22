""" External Modules """
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

# Local Modules
from checkout_app.webhook_handler import StripeWH_Handler

import stripe

@require_POST
@csrf_exempt
def webhook(request):
    """Listen for webhooks from Stripe"""
    # Setup
    wh_secret = settings.STRIPE_WH_SECRET
    stripe.api_key = settings.STRIPE_SECRET_KEY_BOUTIQUE

    # Get the webhook data and verify its signature
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    # Originally from django
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, wh_secret
            )
    
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)
    
    # Generic exception to catch any other than what stripe has provided
    except Exception as e:
        return HttpResponse(content=e, status=400)


# can make our work reusable such that we can:
# import it into other projects,
# Subclass it to override the methods
# Or even open-source it and share it publicly.

    # Custom content to set up an instance of our webhook handler
    handler = StripeWH_Handler(request)

    # Map webhook events dictionary to relevant handler methods inside StripeWH_Handler
    event_map = {
        'payment_intent.succeeded': handler.handle_payment_intent_succeeded,
        'payment_intent.payment_failed': handler.handle_payment_intent_payment_failed,
    }

    # Get the webhook event from Stripe
    event_type = event['type']

    # If there's a handler for it, get it from the event map
    # or use the generic one by default
    event_handler = event_map.get(event_type, handler.handle_event)

# event_handler is nothing more than an alias for whatever function we pulled out of the event_map
# dictionary. This means we can call it just like any other function. So to get the response from
# the webhook handler, we just call event_handler, and pass it the event:

    # Call the event handler with the event
    response = event_handler(event)
    return response
