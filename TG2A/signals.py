from .models import gallery
from django.db.models.signals import post_delete
from django.core.signals import request_finished
from django.dispatch import receiver
import os


@receiver(post_delete, sender=gallery)
def my_callback(sender, instance, **kwargs):
    if instance.image:
        instance.image.delete(save=False)

    try:
        os.remove(instance.thumbnail_url[1:]) # Has to be a relative path.
    except OSError as error:
        print(error)
