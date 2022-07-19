from datetime import datetime, timedelta
from django.utils import timezone
from .models import Msa, r_request
from django.contrib.auth.models import User

from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job

scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), "default")

# Every one hour query for users/rooms and messages that are older than one hour then delete them
@register_job(scheduler, "interval", seconds=3600, id="delete_object", replace_existing=True)
def delete_object():
    for object in Msa.objects.all():
        time_elapsed = timezone.now() - object.created_time

        if time_elapsed > timedelta(hours=1):
            object.delete()


    for users in User.objects.filter(is_active='False'):
        time_elapsed = timezone.now() - users.date_joined
        if time_elapsed > timedelta(hours=1):            
            users.delete()

    for rooms in r_request.objects.all():
        time_elapsed = timezone.now() - rooms.created_time

        if time_elapsed > timedelta(hours=1):
            rooms.delete()

register_events(scheduler)
