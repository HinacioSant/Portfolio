from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from login.user_management import user_m
from .chat_management import chat_m, rooms_r, error_check
from .models import Msa, r_request, Friend
from .encryption_util import decrypt

# Create your views here.

def msaindex(request): # MSA index page
    response = error_check(request=request, error="403")

    if response == "redirect":
        return redirect('msa_menu')

    if request.method == "POST": # Creating a Temporay user

        response = user_m(form=request.POST).temporary_user() # (Temporay user creation) Class outside views, see: User_management.py to more info.

        if response == 'User already exists': # If the user already exist
            return redirect('msa')# Redirect

        request.session.set_expiry(3600) # Set the cookie to expire in one hour.
        request.session['name'] = request.POST['username'] # add the user to session.

        return redirect('msa_menu') # Return to the user menu after creation.


    return render(request, "MSA/msaindex.html")# Render template


def msa_menu(request): # User/Overall menu
    response = error_check(request=request, error="401")

    if response == "redirect":
        return redirect('msa')

    friendlist = Friend.objects.filter(user=response)
    userlist =  User.objects.filter(is_active=False).exclude(Friend_friendlist__in=friendlist) # list of temporary users that you can chat with.


    if request.method == "POST":
        if request.POST["action"] == "unfriend":
            response2 = chat_m(data=request.POST["friend_id"]).delete_friend()

            if response2 == "Invalid Object":
                return redirect(msa_menu)
        else:
            user = response # If no error is found error_check return the User object.
            user2 = request.POST["user2_id"]
            data = {"user": user, "user2": user2}

            response2 = chat_m(data=data).add_friend()
            if response2 == "Invalid User" or response2 == "object already exists":
                return redirect(msa_menu)

    context = {
        "user1": response,
        "list": userlist,
        "friendlist": friendlist,
    }

    return render(request, "MSA/msa_menu.html",context) # Render template

def chat(request, id1, id2): # Chat page (id variable to room creation)
    response = error_check(id1=id1, id2=id2, request=request, error="423")

    if response == "redirect_msa":
        return redirect('msa')

    elif response == "redirect_menu":
        return redirect('msa_menu')

    else:
        user = response['user']
        user2 = response['user2']

        room = id1+id2 # Variable added to easier use
        response = rooms_r(room=room, id1=id1, id2=id2).rooms() # (Room creation) Class outside views, check chat_management.py for more info.

        if response == "room already exists":
            room2 = id2+id1
            return render(request, "MSA/chat.html", {"id1": id2, "id2": id1, "name": user.username, "user2":user2,"room": room2,})

    context ={
        "id1":id1,
        "id2":id2,
        "name": user.username,
        "user2": user2,
        "room": room,
    }

    return render(request, "MSA/chat.html", context) # Render template


def messages(request, id1, id2): # Message page(add/query and deploy of messages)(Variables to query)
    response = error_check(id1=id1, id2=id2, request=request, error="423")

    if response == "redirect_msa":
        return redirect('msa')

    elif response == "redirect_menu":
        return redirect('msa_menu')

    else:
        room_r = id1+id2 # Variable added to easier use.
        room = r_request.objects.get(room=room_r)

        data = Msa.objects.filter(room = room) # Messages query.

        messages_dict = {"messages":[]}
        for a in data:                                               # Decrypt content before showing the message to the user. Check(encryption_ultil.py for more info)
            messages_dict['messages'].append({"user": a.user.username, "content": decrypt(a.content), "time": a.created_time.strftime("%H:%M:%S")})

    if request.method == "POST": # New message
        chat_m(data=request.POST).msg(room=room) # (Message creation) Class outside views, check chat_management.py for more info.

    return JsonResponse(messages_dict) # Return a serialized list as a json response

def room_request(request): # Room query page (handle the invite to enter a room)
    try: # Checks if the user is on the database
        user = User.objects.get(username=request.session['name'])

        data = r_request.objects.filter(request_to=user.id) # Room request query

        requests_dict = {"requests":[]}
        for a in data:
            requests_dict['requests'].append({"request_from": a.request_from.id, "request_to": a.request_to.id, "room": a.room})

    except ObjectDoesNotExist: # If not
        return redirect('msa') # Redirect

    return JsonResponse(requests_dict) # Return a serialized list of the rooms that the user was invited to in json response.


def search(request): # Search for user (redirection to room creation)
    if request.method == 'POST': # Only handle POST requests
        id1 = request.POST['id1'] # Variable added to easier use
        id2 = request.POST['id2'] # Variable added to easier use
        room = id1 + "/"+ id2 # Variable added to easier use

        return redirect('chat/'+room) # Redirect to the room
    else:
        return redirect('msa') # If not a POST request redirect to the index page

def check(request, new_check): # Page to check if there is new rooms/messages to be added to the user.
    user = User.objects.get(username=request.session['name'])
    response = {}
    if new_check == "room": # Room
        try:
            rooms = r_request.objects.filter(request_to=user).latest("request_from")
            response = {"new_requests": "yes", "room": rooms.request_from.id}
        except ObjectDoesNotExist:
            pass

    else: # Messages
        try:
            room = r_request.objects.get(room=new_check)
            chat = Msa.objects.filter(room=room).latest("created_time")
            response = {"new_messages": "yes", "time": chat.created_time.strftime("%H:%M:%S")}
        except ObjectDoesNotExist:
            pass

    return JsonResponse(response)
