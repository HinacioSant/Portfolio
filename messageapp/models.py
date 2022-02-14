from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class r_request(models.Model):
    room = models.IntegerField()
    created_time = models.DateTimeField(default=timezone.now, blank=True)
    request_from = models.ForeignKey(User, on_delete=models.CASCADE, related_name="User_request_form")
    request_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name="User_request_to")

    def __str__(self):
        return '{}'.format(self.room)

class Msa(models.Model):
    room = models.ForeignKey(r_request, on_delete=models.CASCADE)
    created_time = models.DateTimeField(default=timezone.now, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=500)


    def __str__(self):
        return 'Room: {}'.format(self.room)

class Friend(models.Model):
    user =  models.ForeignKey(User, on_delete=models.CASCADE, related_name="User_friendlist")
    friend =  models.ForeignKey(User, on_delete=models.CASCADE, related_name="Friend_friendlist")
