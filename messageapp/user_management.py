from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist


class user_g: # User Creation
    def __init__(self, name, status):
        self.name = name
        self.status = status

    def add(self): # Add user function
        try: # Checks if the user already exists
            User.objects.get(username=self.name)
            response = 'User already exists' # If so
            return response # Return response
        except ObjectDoesNotExist: # If not
            add = User(username=self.name, is_active=self.status) # Create User
            add.save()
