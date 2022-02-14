from .models import Msa, r_request, Friend
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from .encryption_util import encrypt


class chat_m: # Message creation
    def __init__(self, data):
        self.data = data

    def msg(self, room): # Add message function

        check = Msa.objects.filter(room = room) # Variable added to easie use

        if len(check) >= 5: # Checks if there are more than/or 5 messages
            d = Msa.objects.filter(room = room)[:1].get() # If so
            d.delete() # Delete the oldest message

        user = User.objects.get(username=self.data["name"])
        content = encrypt(self.data["content"]) # Encrtypt the content before adding
                                                # to the database. Check(encryption_ultil.py for more info)


        add = Msa(room = room, user=user, content=content) # Add a new message
        add.save()

    def add_friend(self):
        try: # Check if the object already exist.
            Friend.objects.get(friend=self.data["user2"])
            response = "object already exists"

            return response

        except ObjectDoesNotExist:
            pass

        try: # Add object.
            user = self.data["user"]
            user2 = User.objects.get(id=self.data["user2"])

            add = Friend(user=user, friend=user2)
            add.save()

        except ObjectDoesNotExist:
            response =  "Invalid User"
            return response

    def delete_friend(self):
        try: # Delete object.
            delete = Friend.objects.get(id=self.data)
            delete.delete()

        except ObjectDoesNotExist:
            response =  "Invalid Object"
            return response


class rooms_r: # Room creation
    def __init__(self, room, id1, id2):
        self.room = room
        self.id1 = User.objects.get(id= id1)
        self.id2 = User.objects.get(id= id2)



    def rooms(self): # Add room function
        try: # Check if the room already exists
            room2 = str(self.id2.id)+str(self.id1.id)
            r_request.objects.get(room = room2)
            return "room already exists"
        except ObjectDoesNotExist: # If not
            pass

        try: # Check if the room already exists
            r_request.objects.get(room = self.room)

        except ObjectDoesNotExist: # If not
            add = r_request(room = self.room, request_from = self.id1, request_to = self.id2) # Create new room
            add.save()


def error_check(**kwargs):
    error = kwargs.get("error")

    if kwargs.get("request"):
        request = kwargs.get("request")


    if kwargs.get("id1"):
        id1 = kwargs.get("id1")

    if kwargs.get("id2"):
        id2 = kwargs.get("id2")

    if error == "401":

        try: # Checks if the user is in session
            if request.session['name']: # If it is
                pass
        except KeyError: # Else
            response = "redirect" # Redirect
            return response


        try: # If the user is not on the database
            user = User.objects.get(username=request.session['name'])
            response = user
            return response

        except ObjectDoesNotExist: # Redirect to the index
            response = "redirect"
            return response

    if error == "403":

        try: # If user in session
            if request.session['name']:
                response = "redirect" # Redirect
                return response

        except KeyError: # If not
            if request.user.is_authenticated:
                request.session['name'] = request.user.username

                response = "redirect" # Redirect
                return response

    if error == "423":

        try: # Checks if the user is in session
            if request.session['name']: # If it is
                pass
        except KeyError: # Else
            response = "redirect_msa"
            return response

        try: # Checks if the user is on the database

            user = User.objects.get(id=id1)
            user2 = User.objects.get(id=id2)

            if str(user.id) != id1 and str(user.id) != id2: # Checks if user is one of the user on the room.
                response = "redirect_menu"
                return response
            else:
                response = {"user": user, "user2": user2}
                return response

        except ObjectDoesNotExist:
            response = "redirect_msa"
            return response
