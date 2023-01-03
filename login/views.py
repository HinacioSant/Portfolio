from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from TG2A.models import reports
from django.conf import settings
from django.contrib.auth import logout as log_out       # Set to custom name to easier and non conflictual use
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from .user_management import user_m  # Set to custom name to easier use.
from django.utils import timezone


def home(request):  # Home page
    return render(request, "login/home.html")

def register(request): # Register page
    if request.method == "POST":

        response = user_m(form=request.POST).register() # Use the register method inside user_management.py to register.(Check user_management.py for more info.)

        if response == "User name exists": # If it returns a error
            return render(request, "login/register.html", {"validation_username": "is-invalid"})   # Render the page with the error message.

        if response == "Email exists":
            return render(request, "login/register.html", {"validation_email": "is-invalid"})   # Render the page with the error message.

        if response == "redirect": # If not
            return redirect("/login") # redirect to /login.

    elif request.user.is_authenticated: # If not a post request and the user is already logged
        return redirect("/home")           # redirects them to the home page.

    return render(request, "login/register.html")   #Render of the page


def login(request): # Login page
    a = reports(image_id = "Login_pageview", reason = "Guest use", more_info = timezone.now().strftime("%Y-%m-%d %H:%M:%S"))
    a.save()

    if request.method == "POST":
        response = user_m(form=request.POST).login(request_login=request) # Use the login method inside user_management.py to login.(Check user_management.py for more info.)

        if response == "captcha error!":  # If it returns a error
            return render(request, "login/login.html", {'error': "Captcha error!!, try again!"})    # Render the page with the error message.

        elif response == "User doesn't exists":
            return render(request, "login/login.html", {"validation_username": "is-invalid"})   # Render the page with the error message.

        elif response == "invalid password":
            return render(request, "login/login.html", {'validation_password': "is-invalid"})   # Render the page with the error message.

        elif response == "redirect": # If not
            return redirect("/home") # redirect to /home.

    elif request.user.is_authenticated: # If not a post request and the user is already logged
        return redirect("/home")            # redirects them to the home page.


    return render(request, "login/login.html") # Render of the page.

def lg(request):
    form = {}
    form["username"] = "Guest"
    form["password1"] = "jorge223"

    response = user_m(form=form).login(request_login=request)
    a = reports(image_id = "1", reason = "Guest use", more_info = timezone.now().strftime("%Y-%m-%d %H:%M:%S"))

    a.save()

    return redirect("/projects")

@login_required # If the user is not logged redirects them to the home page.
def password_change(request): # Password change page
    if request.method == 'POST':
        response = user_m(form=request.POST).change_password(user=request.user) # Use the change_password method inside user_management.py to change password.(Check user_management.py for more info.)

        if response == "continue": # If no error occours
            return render(request, "login/password_change_done.html") # render the password change done page.

        elif response == "invalid": # Else
            return render(request, "login/password_change.html", {'old_password_validation': "is-invalid"}) # Render the page with the error message.


    return render(request, "login/password_change.html") # Render of the page



def logout(request): # Logout page
    log_out(request) # uses the django logout fuction to logout users on both the social based login and the login page login
    return redirect("/home") # them redirects to the home page.
