"""
these signals are sent by django to the entire application
after a model instance is saved and after it's deleted
"""
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import OrderLineItem


# to execute this function anytime the post_save signal is sent
# Receiving post_save signals from the OrderLineItem model:
@receiver(post_save, sender=OrderLineItem)
def update_on_save(sender, instance, created, **kwargs):
    """
    Special function to handle signals from the post_save event.
    Update order total on lineitem update / create.
    """
    print('save signal received!')
    instance.order.update_total()


@receiver(post_delete, sender=OrderLineItem)
def update_on_delete(sender, instance, **kwargs):
    """
    Special function to handle signals from the post_save event.
    Update order total on lineitem delete.
    """
    print('delete signal received!')
    instance.order.update_total()
