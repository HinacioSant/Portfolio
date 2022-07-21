from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import login as sign_in        # Set to custom name to easier and non conflictual use
import requests
import json



class user_m:
    def __init__(self, form):
        self.form = form

    def username_check(self): # This method checks the validity of the username within the database.
        try:                  # This method is used both in the login and in register authentication.
            user = User.objects.get(username=self.form['username'])  # Checks if the username already exist

            if user:  # If so return a 409 code and the context that can be use to identificate which is which.
                response = {"409": True, "context": "User name exists", "user": user} # In this case also returns the user.
                return response

        except ObjectDoesNotExist: # if not, return a 409 code and the context that can be use to identificate which is which.
            return {"409": False, "context": "User doesn't exists"}



    def email_check(self): # This method does basically the same thing with email.
        try:
            email = User.objects.get(email=self.form['email']) # Checks if the email already exist

            if email:  # If so return a 409 code and the context that can be use to identificate which is which.
                response = {"409": True, "context": "Email exists", "email": email}
                return response

        except ObjectDoesNotExist:
            return {"409": False, "context": "Email doesn't exists"}



    def register(self): # This is the registration method, all logic behind registration is within this method.
        username = self.form['username']
        email = self.form['email']
        password1 = self.form['password1']
        password2 = self.form['password2']

        response = self.username_check() # Use the username_check method to check the validity.
        if response['409']: # If 409 error
            return response['context'] # return the context.

        response = self.email_check() # Same in here but with the email_check method.
        if response['409']:
            return response['context']

        hash = make_password(password1) # Hashes the password using django base hash that can be changed on settings.


        add = User(email = email, username = username, password = hash) # Adds and
        add.save()   # save to the database.

        response = "redirect"
        return response   # Then redirects to the login page.



    def login(self, request_login): # This is the login method, all logic behind login is within this method.
        # request_login variable is added to login using django sign_in method.
        # Google captcha verification

        # Setting the google Recaptcha api.
        captcha_token = self.form['g-recaptcha-response']
        captcha_url = "https://www.google.com/recaptcha/api/siteverify"
        captcha_secret = "6Lc8tAshAAAAAElWtrjAuV8zMnrv_i2JBA-8h3Mi"
        data = {"secret":captcha_secret,"response":captcha_token}
        csr = requests.post(url=captcha_url,data=data) # Catptcha server response

        csr_json = json.loads(csr.text)
         # Loading on json to better read
        if csr_json['success'] != True: # Setting the login conditions of the captcha
            response = "captcha error!"
            return response

        response = self.username_check() # Use the username_check method to check the validity.
        if not response['409']:
            return response['context']

        verification = response['user'] # Set to a variable to easier use.

        if check_password(self.form['password1'], verification.password):  # Using the django check_password to se if the passwords match
            sign_in(request_login, verification, backend='django.contrib.auth.backends.ModelBackend') # if so, sign in

            request_login.session["name"] = request_login.user.username

            return "redirect"                                                            # and redirect to the home page
        else:                                                                                   # if not
            return "invalid password"   # error message  (message on the html side)



    def change_password(self, user): # Change password method.
        verification = User.objects.get(username=user)  # Setting the User object to a variable to easier use.
        # Django check_password method.                                  # To change the password the old one must be input
        if check_password(self.form['old_password'], verification.password):    # checks if the old password is right.

                                                                                            # If all requirements set above are met
            User.objects.filter(username=user).update(password=make_password(self.form['password1'])) # update the password to the new one.
            response = "continue" # And continue.
            return response

        else: # If not
            response = "invalid"
            return response # Return error.



    def temporary_user(self):
        response = self.username_check()
        if response['409']:
            return response['context']

        add = User(username=self.form['username'], is_active=self.form['status']) # Create User
        add.save()
