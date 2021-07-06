from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth import logout as log_out       # Set to custom name to easier and non conflictual use
from django.contrib.auth import login as sign_in        # Set to custom name to easier and non conflictual use
from django.contrib.auth import authenticate as auth    # Set to custom name to easier and non conflictual use
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password
import requests
import json

def home(request):  # Home page
    return render(request, "login/home.html")


def register(request): # Register page
    if request.method == "POST":
        form =  request.POST # Setting the request.POST to a variable to easier use

        try:
            if User.objects.get(username=form['username']):  # Checks if the username already exist
                return render(request, "login/register.html", {'username_validation': "is-invalid"})# if so, show a error message. (message on the html side)
        except ObjectDoesNotExist:              # if not, just continue.
            pass

        try:
            if User.objects.get(email=form['email']):   # Same thing but with the email.           # The email must be unique
                return render(request, "login/register.html", {'email_validation': "is-invalid"}) # so the application can send
        except ObjectDoesNotExist:                                                                # the password recover email.
            pass


        if form['password1'] != form['password2']:  # Checks if the passwords are equal, if not:
            return render(request, "login/register.html", {'password_validation': "is-invalid", "m": True})# Error message (message on the html side)

        elif len(form['password1']) < 6:    # Checks if the password is too short.
            return render(request, "login/register.html", {'password_validation': "is-invalid", "s": True})# Error message (message on the html side)

        elif len(form['password1']) > 64:   # Checks if the password is too long.
            return render(request, "login/register.html", {'password_validation': "is-invalid", "l": True})# Error message (message on the html side)

        first_isalpha = form['password1'].isalpha()   # Checks if the password is all numeric or all letters.
        if all(c.isalpha() == first_isalpha for c in form['password1']): # Loop inside the password to check if all caracteres are letters or numbers                 |
            return render(request, "login/register.html", {'password_validation': "is-invalid"})# Error message| unless the password has both a error message appears.|



        hash = make_password(form['password1']) # Hashes the password using django base hash that can be changed on settings.


        add = User(email = form['email'], username = form['username'], password = hash) # Adds and
        add.save()                                                                     # save to the database.
        return redirect("/login")   # Then redirects to the login page.



    elif request.user.is_authenticated: # If not a post request and the user is already logged
        return redirect("/")            # redirects them to the home page.

    return render(request, "login/register.html")   #Render of the page


def login(request): # Login page
    if request.method == "POST":
        form =  request.POST  # Setting the request.POST to a variable to easier use

        # Google captcha verification
        captcha_token = form['g-recaptcha-response']                    #setting the google Recaptcha api.
        captcha_url = "https://www.google.com/recaptcha/api/siteverify"
        captcha_secret = "6LfY6YwaAAAAAH1PHsBNPyV_qlNJQthY9OXChL2v"
        data = {"secret":captcha_secret,"response":captcha_token}
        csr = requests.post(url=captcha_url,data=data) # Catptcha server response

        csr_json = json.loads(csr.text) # Loading on json to better read
        if csr_json['success'] != True: # Setting the login conditions of the captcha
            return render(request, "login/login.html", {'error': "Captcha error!!, try again!"})    # Error message if not met
        if csr_json['score'] < 0.5: # Setting the login conditions of the captcha
            return render(request, "login/login.html", {'error': "Captcha error!!, try again!"})    # Error message if not met


        try:
            verification = User.objects.get(username=form['username']) # Checks if the username exist
        except ObjectDoesNotExist:                                     # if not
            return render(request, "login/login.html", {'username_validation': "is-invalid"}) # error message. (message on the html side)


        if check_password(form['password1'], verification.password):  # Using the django check_password to se if the passwords match
            sign_in(request, verification, backend='django.contrib.auth.backends.ModelBackend') # if so, sign in
            return redirect("/home")                                                            # and redirect to the home page
        else:                                                                                   # if not
            return render(request, "login/login.html", {'password_validation': "is-invalid"})   # error message  (message on the html side)



    elif request.user.is_authenticated: # If not a post request and the user is already logged
        return redirect("/")            # redirects them to the home page.


    return render(request, "login/login.html") # Render of the page.


@login_required # If the user is not logged redirects them to the home page.
def password_change(request): # Password change page
    if request.method == 'POST':
        form = request.POST     # Setting the request.POST to a variable to easier use


        verification = User.objects.get(username=request.user)  # Setting the User object to a variable to easier use.
                                                                            # To change the password the old one must be input
        if check_password(form['old_password'], verification.password):     # checks if the old pássword is right.

            if form['new_password1'] != form['new_password2']:  # Checks if the new passwords are equal, if not
                return render(request, "login/password_change.html", {'new_password_validation': "is-invalid", "m": True}) # error message. (message on the html side)

            if len(form['new_password1']) < 6:  # Checks if the new passwords are too short, if so
                return render(request, "login/password_change.html", {'new_password_validation': "is-invalid", "s": True}) # error message. (message on the html side)
            if len(form['new_password1']) > 64: # Checks if the new passwords are too long, if so
                return render(request, "login/password_change.html", {'new_password_validation': "is-invalid", "l": True}) # error message. (message on the html side)

            first_isalpha = form['new_password1'].isalpha() # Checks if the new password is all numeric or all letters.
            if all(c.isalpha() == first_isalpha for c in form['new_password1']):  # Loop inside the password to check if all caracteres are letters or numbers
                return render(request, "login/password_change.html", {'new_password_validation': "is-invalid"})# Error message| unless the password has both a error message appears.|
                                                                                                            # If all requirements set above are met
            User.objects.filter(username=request.user).update(password=make_password(form['new_password1'])) # update the password to the new one.
            return render(request, "login/password_change_done.html") # render the password change done page.

        else:                                                              # if the old password is not right
            return render(request, "login/password_change.html", {'old_password_validation': "is-invalid"}) # error message. (message on the html side)


    return render(request, "login/password_change.html") # Render of the page



def logout(request): # Logout page
    log_out(request) # uses the django logout fuction to logout users on both the social based login and the login page login
    return redirect("/") # them redirects to the home page.
