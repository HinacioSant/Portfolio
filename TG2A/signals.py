from .models import gallery
from django.db.models.signals import post_delete
from django.core.signals import request_finished
from django.dispatch import receiver
import os


@receiver(post_delete, sender=gallery)
def my_callback(sender, instance, **kwargs):
    if instance.image:
        instance.image.delete(save=False)
    if instance.thumbnail_url:
        instance.thumbnail_url.delete(save=False)
