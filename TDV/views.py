from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import notes
from .notes_management import notes_management

# Create your views here.

def tdv(request):
    return render(request, "TDV/tdv.html")


def notes_page(request):

    if request.method == 'POST':
        response = notes_management(form=request.POST, user=request.user).bullet_management()
        if response == "redirect_notes":
            return redirect("notes_page")


    notes_list =  notes.objects.filter(user=request.user, type="note")
    bullet_list = notes.objects.filter(user=request.user, type="bullet")


    context = {
        "notes_list": notes_list,
        "bullet_list": bullet_list,
    }
    return render(request, "TDV/notes_page.html", context)


def add_notes(request):
    if request.method == 'POST':
        response = notes_management(form=request.POST, user=request.user).notes_add()
        if response == "redirect_notes":
            return redirect("notes_page")



    context = {
        "content": ""
    }
    return render(request, "TDV/add_notes.html", context)
