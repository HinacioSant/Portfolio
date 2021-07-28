from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from . import user_management as um
from . import chat_management as cm
from .models import Msa, r_request
from django.core import serializers
from datetime import datetime
from django.contrib.auth.decorators import login_required
# Create your views here.

def msaindex(request):
    try :
        if request.session['name']:
            return redirect('msa_menu')
    except KeyError:
        pass

    if request.method == "POST":
        form = request.POST
        request.session['name'] = form['iname']
        response = um.user_g(name=form['iname'], status='False').add()
        if response == 'User already exists':
            print(response)
            return redirect('msa')

        return redirect('msa_menu')



    return render(request, "MSA/msaindex.html")


def msa_menu(request):
    try :
        if request.session['name']:
            pass
    except KeyError:
        return redirect('msa')


    user = User.objects.get(username=request.session['name'])

    context = {
        "user1": user,
        "list": User.objects.filter(is_active=False),
    }

    return render(request, "MSA/msa_menu.html",context)

def chat(request, id1, id2):
    try :
        if request.session['name']:
            pass
    except KeyError:
        return redirect('msa')
    user = User.objects.get(username=request.session['name'])
    if str(user.id) != id1 and str(user.id) != id2:
        return redirect('msa_menu')



    room = id1+id2
    cm.rooms_r(room=room, id1=id1, id2=id2).rooms()

    context ={
        "id1":id1,
        "id2":id2,
        "time": datetime.now().strftime("%d/%b/%Y, %H:%M:%S"),
        "name": user.username
    }

    return render(request, "MSA/chat.html", context)


def messages(request, id1, id2):
    try :
        if request.session['name']:
            pass
    except KeyError:
        return redirect('msa')
    user = User.objects.get(username=request.session['name'])
    if str(user.id) != id1 and str(user.id) != id2:
        return redirect('msa_menu')



    room = id1+id2
    data = Msa.objects.filter(room = room)

    if request.method == "POST":
        form = request.POST
        cm.chat(room = room, user = form['name'], content= form['content'], time = form['time']).msg()

    return JsonResponse({"messages": list(data.values())})

def room_request(request):
    user = User.objects.get(username=request.session['name'])
    data = r_request.objects.filter(request_to=user.id)


    return JsonResponse({"requests": list(data.values())})
