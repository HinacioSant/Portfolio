from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from . import user_management as um
from . import chat_management as cm
from .models import Msa, r_request
from django.core import serializers
from datetime import datetime
# Create your views here.

def msaindex(request): # MSA index page
    try: # If user in session
        if request.session['name']:
            return redirect('msa_menu') # Redirect to the user menu
    except KeyError: # If not
        pass

    if request.method == "POST": # Creating a new user
        form = request.POST # Variable added to easier use
        response = um.user_g(name=form['iname'], status='False').add() #(user creation) Class outside views, see: User_management.py to more info.
        if response == 'User already exists': # If the user already exist
            return redirect('msa')# Redirect

        request.session.set_expiry(3600) # Set the cookie to expire in one hour.
        request.session['name'] = form['iname'] # add the user to session.

        return redirect('msa_menu') # Return to the user menu after creation.


    return render(request, "MSA/msaindex.html")# Render template


def msa_menu(request): # User/Overall menu
    try: # Checks if the user is in session
        if request.session['name']: # If it is
            pass
    except KeyError: # Else
        return redirect('msa') # Redirect

    try: # If the user is not on the database
        user = User.objects.get(username=request.session['name'])


    except ObjectDoesNotExist: # Redirect to the index
        return redirect('msa')

    context = {
        "user1": user,
        "list": User.objects.filter(is_active=False),
    }

    return render(request, "MSA/msa_menu.html",context) # Render template

def chat(request, id1, id2): # Chat page (id variable to room creation)
    try: # Checks if the user is in session
        if request.session['name']: # If it is
            pass
    except KeyError: # Else
        return redirect('msa') # Redirect

    try: # Checks if the user is on the database
        user = User.objects.get(username=request.session['name'])
        if str(user.id) != id1 and str(user.id) != id2: # Checks if user is one of the user on the room.
            return redirect('msa_menu') # If not redirect


        room = id1+id2 # Variable added to easier use
        cm.rooms_r(room=room, id1=id1, id2=id2).rooms() # (Room creation) Class outside views, check chat_management.py for more info.


    except ObjectDoesNotExist: # If not
        return redirect('msa') # Redirect

    context ={
        "id1":id1,
        "id2":id2,
        "time": datetime.now().strftime("%d/%b/%Y, %H:%M:%S"),
        "name": user.username
    }

    return render(request, "MSA/chat.html", context) # Render template


def messages(request, id1, id2): # Message page(add/query and deploy of messages)(Variables to query)
    try: # Checks if the user is in session
        if request.session['name']: # If it is
            pass
    except KeyError: # Else
        return redirect('msa') # Redirect

    try: # Checks if the user is on the database
        user = User.objects.get(username=request.session['name'])
        if str(user.id) != id1 and str(user.id) != id2: # Checks if user is one of the user on the room.
            return redirect('msa_menu') # If not redirect



        room = id1+id2 # Variable added to easier use.
        data = Msa.objects.filter(room = room) # Messages query.

    except ObjectDoesNotExist: # If not
        return redirect('msa') # Redirect

    if request.method == "POST": # New message
        form = request.POST # Variable added to easier use.
        cm.chat(room = room, user = form['name'], content= form['content'], time = form['time']).msg() # (Message creation) Class outside views, check chat_management.py for more info.

    return JsonResponse({"messages": list(data.values())}) # Return a serialized list as a json response

def room_request(request): # Room query page (handle the invite to enter a room)
    try: # Checks if the user is on the database
        user = User.objects.get(username=request.session['name'])
        data = r_request.objects.filter(request_to=user.id) # Room request query

    except ObjectDoesNotExist: # If not
        return redirect('msa') # Redirect

    return JsonResponse({"requests": list(data.values())}) # Return a serialized list of the rooms that the user was invited to in json response.


def search(request): # Search for user (redirection to room creation)
    if request.method == 'POST': # Only handle POST requests
        id1 = request.POST['id1'] # Variable added to easier use
        id2 = request.POST['id2'] # Variable added to easier use
        room = id1 + "/"+ id2 # Variable added to easier use

        return redirect('chat/'+room) # Redirect to the room
    else:
        return redirect('msa') # If not a POST request redirect to the index page
