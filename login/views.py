from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth import logout as log_out       # Set to custom name to easier and non conflictual use
from django.contrib.auth.decorators import login_required
from .user_management import user_m

def home(request):  # Home page
    return render(request, "login/home.html")

def register(request): # Register page
    if request.method == "POST":
        response = user_m(form=request.POST).register()
        if response == "User name exists":
            return render(request, "login/register.html", {"validation_username": "is-invalid"})   #Render of the page

        if response == "Email exists":
            return render(request, "login/register.html", {"validation_email": "is-invalid"})   #Render of the page

        if response == "redirect":
            return redirect("/login")

    elif request.user.is_authenticated: # If not a post request and the user is already logged
        return redirect("/home")           # redirects them to the home page.

    return render(request, "login/register.html")   #Render of the page


def login(request): # Login page
    if request.method == "POST":
        response = user_m(form=request.POST).login(request_login=request)

        if response == "captcha error!":
            return render(request, "login/login.html", {'error': "Captcha error!!, try again!"})    # Error message if not met

        elif response == "User doesn't exists":
            return render(request, "login/login.html", {"validation_username": "is-invalid"})   #Render of the page

        elif response == "redirect":
            return redirect("/home")

        elif response == "invalid password":
            return render(request, "login/login.html", {'validation_password': "is-invalid"})   # error message  (message on the html side)

    elif request.user.is_authenticated: # If not a post request and the user is already logged
        return redirect("/home")            # redirects them to the home page.


    return render(request, "login/login.html") # Render of the page.


@login_required # If the user is not logged redirects them to the home page.
def password_change(request): # Password change page
    if request.method == 'POST':
        response = user_m(form=request.POST).change_password(user=request.user)

        if response == "continue":
            return render(request, "login/password_change_done.html") # render the password change done page.
        elif response == "invalid":
            return render(request, "login/password_change.html", {'old_password_validation': "is-invalid"}) # error message. (message on the html side)


    return render(request, "login/password_change.html") # Render of the page



def logout(request): # Logout page
    log_out(request) # uses the django logout fuction to logout users on both the social based login and the login page login
    return redirect("/home") # them redirects to the home page.
