from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import notes
from .notes_management import notes_management


# Create your views here.

def tdv(request): # Index page.
    return render(request, "TDV/tdv.html")


def notes_page(request): # Note page (management of bullets(delete/if is finished)).


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



    context = {
        "content": "" # add explication
    }
    return render(request, "TDV/add_notes.html", context)



def edit_note(request, note_id): # Edit notes page.
    if request.method == 'GET': # If get request (page only accessible through post request )
        return redirect("notes_page") # Redirect.

    if request.method == 'POST': # If post request.
        form = request.POST # Added variable for easier use.

        if form["type"] == "fill":  # If the post request come with "type: fill"
            title = form["title_n"] # Just fill in the respective places. (Title)
            subject = form["subject_n"] # Subject
            content = form["content_n"] # Content.

        else: # Else update the object.
            notes.objects.filter(id=note_id).update(title=form["title"], subject=form["subject"], content=form["content"]) # Outside views check notes_management.py for more info.
            return redirect("notes_page") # Then redirect.


    context = { # Fill in the template.
        "id_n": note_id,
        "title": title,
        "subject": subject,
        "content": content,
    }
    return render(request, "TDV/edit_note.html", context)
