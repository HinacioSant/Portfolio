from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist


class user_g:
    def __init__(self, name, status):
        self.name = name
        self.status = status

    def add(self):
        try:
            User.objects.get(username=self.name)
            response = 'User already exists'
            return response
        except ObjectDoesNotExist:
            add = User(username=self.name, is_active=self.status)
            add.save()

    def del_user(self):
        try:
            User.objects.get(username=self.name, is_active=self.status).delete()

        except ObjectDoesNotExist:
            print('not ')
            pass
