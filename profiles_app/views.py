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
