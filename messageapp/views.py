from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse, HttpResponse
from login.user_management import user_m
from .chat_management import chat_m, rooms_r, error_check
from .models import Msa, r_request, Friend
from .encryption_util import decrypt
from TG2A.models import reports
from django.utils import timezone


# Create your views here.

def msaindex(request): # MSA index page
    a = reports(image_id = "MSA_pageview", reason = "Guest use", more_info = timezone.now().strftime("%Y-%m-%d %H:%M:%S"))
    a.save()

    response = error_check(request=request, error="403") # Error handler at chat_management.py

    if response == "redirect":
        return redirect('msa_menu')

    if request.method == "POST": # Creating a Temporay user

        response = user_m(form=request.POST).temporary_user() # (Temporay user creation) Class outside views, see: User_management.py to more info.
        if response == 'User name exists': # If the user already exist
            return render(request, "MSA/msaindex.html", {"error": response})# Redirect

        request.session.set_expiry(3600) # Set the cookie to expire in one hour.
        request.session['name'] = request.POST['username'] # add the user to session.

        return redirect('msa_menu') # Return to the user menu after creation.


    return render(request, "MSA/msaindex.html")# Render template


def msa_menu(request): # User/Overall menu
    response = error_check(request=request, error="401") # Error handler at chat_management.py


    if response == "redirect":
        return redirect('msa')

    # Querying the users for the tables in Msa Menu.

    # Friend list
    friendlist = Friend.objects.filter(user=response)
    # Temporary users list
    userlist =  User.objects.filter(is_active=False).exclude(Friend_friendlist__in=friendlist) # list of temporary users that you can chat with.
    # Resgister users list
    userlist2 =  User.objects.filter(is_active=True).exclude(Friend_friendlist__in=friendlist) # list of non-temporary users that you can chat with.


    context = {
        "user1": response, # If no error occours return the user object as a response
        "list": userlist,
        "friendlist": friendlist,
        "list2": userlist2,
    }

    return render(request, "MSA/msa_menu.html",context) # Render template

def chat(request, id1, id2): # Chat page (id variable to room creation)
    response = error_check(id1=id1, id2=id2, request=request, error="423") # Error handler at chat_management.py

    if response == "redirect_msa":
        return redirect('msa')

    elif response == "redirect_menu":
        return redirect('msa_menu')

    else:
        user = response['user']  # Return users if no error occours
        user2 = response['user2']  # Return users if no error occours

        room = id1+id2 # Variable added to easier use
        response = rooms_r(room=room, id1=id1, id2=id2).rooms() # (Room creation) Class outside views, check chat_management.py for more info.

        if response == "room already exists": # If the room was created by the other user
            room2 = id2+id1                   # render the template a little different .
            return render(request, "MSA/chat.html", {"id1": id2, "id2": id1, "user": user, "user2":user2,"room": room2,})

    context ={
        "id1":id1,
        "id2":id2,
        "user":user,
        "user2": user2,
        "room": room,
    }

    return render(request, "MSA/chat.html", context) # Render template


def messages(request, id1, id2): # Message page(add/query and deploy of messages)(Variables to query)
    response = error_check(id1=id1, id2=id2, request=request, error="423") # Error handler at chat_management.py

    if response == "redirect_msa":
        return redirect('msa')

    elif response == "redirect_menu":
        return redirect('msa_menu')

    else:
        room_r = id1+id2 # Variable added to easier use.
        room = r_request.objects.get(room=room_r)

        user = User.objects.get(username=request.session['name'])

        data = Msa.objects.filter(room = room) # Messages query
        # Query not seen messages
        seen_msgs = Msa.objects.filter(room = room, seen=False).exclude(user=user)

        # Query the room object(can't be sliced for the update)
        room_nw = r_request.objects.filter(room=room_r)


        if seen_msgs : # If there a check for new messages it sets the
                    # field new_messages in r_request to false and mark every message as seen.( the check only happens with the chat open)
            seen_msgs.update(seen=True)

            room_nw.update(new_messages=False)

        # More efficient this way than using List() and more freedom.
        messages_dict = {"messages":[]} # Set the messages in a dictionary to return as a JsonResponse.
        for a in data:                                               # Decrypt content before showing the message to the user. Check(encryption_ultil.py for more info)
            messages_dict['messages'].append({"user": a.user.username, "content": decrypt(a.content), "time": a.created_time.strftime("%H:%M:%S")})

    if request.method == "POST": # New message
        chat_m(data=request.POST).msg(room=room, nw= room_nw) # (Message creation) Class outside views, check chat_management.py for more info.

    return JsonResponse(messages_dict) # Return a json response

def room_request(request): # Room query page (handle the invite to enter a room)
    try: # Checks if the user is on the database
        user = User.objects.get(username=request.session['name'])

        # If the user wasnt the one creating the room(Fist to start the chat), it can the saved on the database field as request_from, if the user was the creator it is saved as request_to.
        # so query both.
        data = r_request.objects.filter(request_to=user.id, new_messages=True) | r_request.objects.filter(request_from=user.id, new_messages=True)

        requests_dict = {"requests":[]}
        for a in data:
            seen_msgs = Msa.objects.filter(room = a, seen=False).exclude(user=user)
            if seen_msgs:
                if a.request_from == user: # handling if the user was the creator or not.
                    requests_dict['requests'].append({"request_from": a.request_to.id, "request_to": a.request_from.id, "room": a.room, "new_msgs": len(seen_msgs), "msg_from": a.request_to.username})
                else:
                    requests_dict['requests'].append({"request_from": a.request_from.id, "request_to": a.request_to.id, "room": a.room, "new_msgs": len(seen_msgs), "msg_from": a.request_from.username})

    except ObjectDoesNotExist: # If not
        return redirect('msa') # Redirect


    return JsonResponse(requests_dict) # Return a json response.



def check(request, new_check): # Page to check if there is new rooms/messages
                            #  to be added to the user, more efficient way the sending get requests to the messages/room_request page.

    user = User.objects.get(username=request.session['name'])
    response = {}
    if new_check == "room": # Room
        try:    # handling if the user was the creator or not.
            data = r_request.objects.filter(request_to=user.id, new_messages=True)

            if not data:    # handling if the user was the creator or not.
                data = r_request.objects.filter(request_from=user.id, new_messages=True)

            if data: # just returns a dictionary with a string.
                response = {"new_requests": "yes"}

        except ObjectDoesNotExist:
            pass

    else: # Messages.
        try:
            room = r_request.objects.get(room=new_check)
            chat = Msa.objects.filter(room=room).latest("created_time")
                                                # time here is just used as a unique variable
                                                # to see if there is a discrepancy in the last message rendered.
            # just returns a dictionary with a string.
            response = {"new_messages": "yes", "time": chat.created_time.strftime("%H:%M:%S")}
        except ObjectDoesNotExist:
            pass

        except ValueError:
            pass

    return JsonResponse(response)


def friend(request): # a view just to handle add/removing friends
                    # for better efficiecy.
    response = error_check(request=request, error="401")  # Error handler at chat_management.py

    if response == "redirect":
        return redirect('msa')

    if request.method == "POST":
        if request.POST["action"] == "unfriend": # Unfriend action check chat_management.py for more info.
            response2 = chat_m(data=request.POST["friend_id"]).delete_friend()

            if response2 == "Invalid Object":
                return redirect(msa_menu)
        else:  # add friend action check chat_management.py for more info.
            user = response # If no error is found error_check return the User object.
            user2 = request.POST["user2_id"]
            data = {"user": user, "user2": user2}

            response2 = chat_m(data=data).add_friend()
            if response2 == "Invalid User" or response2 == "object already exists":
                return redirect(msa_menu)

    return HttpResponse("200") # Return a http response
