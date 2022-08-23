""" Import Modules """
from django.shortcuts import render, get_object_or_404
from django.contrib import messages

from .models import UserProfile
from .forms import UserProfileForm


def profile(request):
    """ Display the user's profile. """
    profile = get_object_or_404(UserProfile, user=request.user)

    # To handle the POST method to update delivery details in profile.html
    # with the 'profile' we have just retrieved above.
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')

    # To populate profile with the current users profile info:
    form = UserProfileForm(instance=profile)

    # To render an order history
    orders = profile.orders.all()

    template = 'profiles/profile.html'
    context = {
        # 'profile': profile,
        'form': form,
        'orders': orders,
        'on_profile_page': True,  # success message if not on profile page
    }

    return render(request, template, context)


def order_history(request, order_number):
    """
    To render the past orders of the user 
    """
    order = get_object_or_404(Order, order_number=order_number)

    messages.info(request, (
        f'This is a past confirmation for order number {order_number}. '
        'A confirmation email was sent on the order date.'
    ))

    # Using the checkout success template
    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
        'from_profile': True, # So we can check in that template if the user got there via the order history view
    }

    return render(request, template, context)
