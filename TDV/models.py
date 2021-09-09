from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class notes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    subject = models.CharField(max_length=64)
    type = models.CharField(max_length=32)
    content = models.TextField(blank=True)
    time = models.DateTimeField(default=timezone.now(), blank=True)
    finished = models.BooleanField()

    def __str__(self):
        return 'Title: {}'.format(self.title)
