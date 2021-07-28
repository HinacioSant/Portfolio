from .models import Msa, r_request
from django.core.exceptions import ObjectDoesNotExist

class chat:
    def __init__(self, room, user, content, time):
        self.room = room
        self.user = user
        self.content = content
        self.time = time

    def msg(self):
        check = Msa.objects.filter(room = self.room)
        if len(check) >= 5:
            d = Msa.objects.filter(room = self.room)[:1].get()
            d.delete()

        add = Msa(room = self.room, user=self.user, content=self.content, time=self.time)
        add.save()


class rooms_r:
    def __init__(self, room, id1, id2):
        self.room = room
        self.id1 = id1
        self.id2 = id2

    def rooms(self):
        try:
            r_request.objects.get(room = self.room)

        except ObjectDoesNotExist:
            add = r_request(room = self.room, request_from = self.id1, request_to = self.id2)
            add.save()
