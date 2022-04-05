from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import notes
from .notes_management import notes_management
from django.http import HttpResponse



# Create your views here.

def tdv(request): # Index page.
    return render(request, "TDV/tdv.html")


def notes_page(request): # Note page (management of bullets(delete/if is finished)).
    if not request.user.is_authenticated:
        return render(request, "TDV/tdv.html", {"error": True})

    if request.method == 'POST': # If post request.
        # Bullet management.
        response = notes_management(form=request.POST, user=request.user).bullet_management() # Outside views check notes_management.py for more info.
        if response == "redirect_notes": # If response comes back "redirect_notes".
            return redirect("notes_page") # Redirect.

    # Queries for the template.
    notes_list =  notes.objects.filter(user=request.user, type="note") # Notes query.
    bullet_list = notes.objects.filter(user=request.user, type="bullet") # Bullet query.


    context = {
        "notes_list": notes_list,
        "bullet_list": bullet_list,
    }
    return render(request, "TDV/notes_page.html", context)


def add_notes(request): # Add notes page (management of notes(add/delete) and bullets(add)).
    if request.method == 'POST':# If post request.
        
        # Notes management.
        response = notes_management(form=request.POST, user=request.user).notes_add() # Outside views check notes_management.py for more info.
        if response == "redirect_notes": # If response comes back "redirect_notes"
            return redirect("notes_page") # Redirect.

    else:
        return redirect("notes_page") # Redirect.

    return HttpResponse("200")



def edit_note(request, note_id): # Edit notes page.
    if not request.user.is_authenticated:
        return render(request, "TDV/tdv.html", {"error": True})

    note_object = notes.objects.get(id=note_id)

    title = note_object.title
    subject = note_object.subject
    content = note_object.content


    if request.method == 'POST': # If post request.
        form = request.POST # Added variable for easier use.

        notes.objects.filter(id=note_id).update(title=form["title"], subject=form["subject"], content=form["content"])
        return redirect("notes_page") # Then redirect.


    context = { # Fill in the template.
        "id_n": note_id,
        "title": title,
        "subject": subject,
        "content": content,
    }
    return render(request, "TDV/edit_note.html", context)
