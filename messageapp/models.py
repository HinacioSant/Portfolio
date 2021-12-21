from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Msa(models.Model):
    room = models.IntegerField(default=1)
    created_time = models.DateTimeField(default=timezone.now, blank=True)
    user = models.CharField(max_length=20)
    content = models.CharField(max_length=500)
    time = models.CharField(max_length=20)

    def __str__(self):
        return 'Room: {}'.format(self.room)

class r_request(models.Model):
    room = models.IntegerField()
    created_time = models.DateTimeField(default=timezone.now, blank=True)
    request_from = models.IntegerField()
    request_to = models.IntegerField()
