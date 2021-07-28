from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.
class Msa(models.Model):
    room = models.IntegerField(default=1)
    user = models.CharField(max_length=20)
    content = models.CharField(max_length=500)
    time = models.CharField(max_length=20)

    def __str__(self):
        return 'Room: {}'.format(self.room)

class r_request(models.Model):
    room = models.IntegerField()
    request_from = models.IntegerField()
    request_to = models.IntegerField()
