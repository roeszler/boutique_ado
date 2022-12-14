""" Import Models """
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from django_countries.fields import CountryField


class UserProfile(models.Model):
    """ 
    A User profile model for maintaining default
    delivery information and order history.
    """
    # specifies that each user can only have one profile:
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # the delivery information fields we want the user to provide defaults for:
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    default_phone_number = models.CharField(max_length=20, null=True, blank=True)
    default_street_address1 = models.CharField(max_length=80, null=True, blank=True)
    default_street_address2 = models.CharField(max_length=80, null=True, blank=True)
    default_town_or_city = models.CharField(max_length=40, null=True, blank=True)
    default_county = models.CharField(max_length=80, null=True, blank=True)
    default_postcode = models.CharField(max_length=20, null=True, blank=True)
    default_country = CountryField(blank_label='Country', null=True, blank=True)

    # string method to return the user name:
    def __str__(self):
        return self.user.username

# receiver for the post save event from the user model
# to automatically create a
# profile for them if the user has just been created OR
# save the profile to update it if the user already existed:
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Create or update user profile
    """
    if created:
        UserProfile.objects.create(user=instance)
    # Existing users: just save the profile
    instance.userprofile.save()
    
    # UserProfile.objects.create(user=instance)
    