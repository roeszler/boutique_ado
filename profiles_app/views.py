""" Import Modules """
from django.shortcuts import render, get_object_or_404

from .models import UserProfile
from .forms import UserProfileForm


def profile(request):
    """ Display the user's profile. """
    profile = get_object_or_404(UserProfile, user=request.user)

    # To populate profile with the current users profile info:
    form = UserProfileForm(instance=profile)

    # To render an order history
    orders = profile.orders.all()

    template = 'profiles/profile.html'
    context = {
        # 'profile': profile,
        'form': form,
        'orders': orders,
    }

    return render(request, template, context)
