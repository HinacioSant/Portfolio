from .models import Msa, r_request
from django.core.exceptions import ObjectDoesNotExist

class chat: # Message creation
    def __init__(self, room, user, content, time):
        self.room = room
        self.user = user
        self.content = content
        self.time = time

    def msg(self): # Add message function
        check = Msa.objects.filter(room = self.room) # Variable added to easie use
        if len(check) >= 5: # Checks if there are more than/or 5 messages
            d = Msa.objects.filter(room = self.room)[:1].get() # If so
            d.delete() # Delete the oldest message

        add = Msa(room = self.room, user=self.user, content=self.content, time=self.time) # Add a new message
        add.save()


class rooms_r: # Room creation
    def __init__(self, room, id1, id2):
        self.room = room
        self.id1 = id1
        self.id2 = id2

    def rooms(self): # Add room function
        try: # Check if the room already exists
            r_request.objects.get(room = self.room)

        except ObjectDoesNotExist: # If not
            add = r_request(room = self.room, request_from = self.id1, request_to = self.id2) # Create new room
            add.save()
