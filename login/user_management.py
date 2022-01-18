from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import login as sign_in        # Set to custom name to easier and non conflictual use
import requests
import json




class user_g: # User Creation
    def __init__(self, name, status):
        self.name = name
        self.status = status

    def add(self): # Add temporary  user function
        try: # Checks if the user already exists
            User.objects.get(username=self.name)
            response = 'User already exists' # If so
            return response # Return response
        except ObjectDoesNotExist: # If not
            add = User(username=self.name, is_active=self.status) # Create User
            add.save()

class user_m:
    def __init__(self, form):
        self.form = form

    def username_check(self):
        try:
            user = User.objects.get(username=self.form['username'])  # Checks if the username already exist

            if user:  # Checks if the username already exist
                response = {"409": True, "context": "User name exists", "user": user}
                return response
        except ObjectDoesNotExist:              # if not, return true.
            return {"409": False, "context": "User doesn't exists"}

    def email_check(self):
        try:
            email = User.objects.get(email=self.form['email'])
            if email:  # Checks if the username already exist
                response = {"409": True, "context": "Email exists", "email": email}
                return response
        except ObjectDoesNotExist:              # if not, just continue.
            return {"409": False, "context": "Email doesn't exists"}


    def register(self):
        username = self.form['username']
        email = self.form['email']
        password1 = self.form['password1']
        password2 = self.form['password2']

        response = self.username_check()
        if response['409']:
            return response['context']

        response = self.email_check()
        if response['409']:
            return response['context']




        hash = make_password(password1) # Hashes the password using django base hash that can be changed on settings.


        add = User(email = email, username = username, password = hash) # Adds and
        add.save()

        response = "redirect"                                                                   # save to the database.
        return response   # Then redirects to the login page.

    def login(self, request_login):
        # Google captcha verification

        captcha_token = self.form['g-recaptcha-response']                    #setting the google Recaptcha api.
        captcha_url = "https://www.google.com/recaptcha/api/siteverify"
        captcha_secret = "6LdPiu4dAAAAAPdZtj52eCTYW4ayOnLb_kBSO9rL"
        data = {"secret":captcha_secret,"response":captcha_token}
        csr = requests.post(url=captcha_url,data=data) # Catptcha server response

        csr_json = json.loads(csr.text)
         # Loading on json to better read
        if csr_json['success'] != True: # Setting the login conditions of the captcha
            response = "captcha error!"
            return response

        response = self.username_check()
        if not response['409']:
            return response['context']

        verification = response['user']

        if check_password(self.form['password1'], verification.password):  # Using the django check_password to se if the passwords match
            sign_in(request_login, verification, backend='django.contrib.auth.backends.ModelBackend') # if so, sign in
            return "redirect"                                                            # and redirect to the home page
        else:                                                                                   # if not
            return "invalid password"   # error message  (message on the html side)

    def change_password(self, user):
        verification = User.objects.get(username=user)  # Setting the User object to a variable to easier use.
                                                                            # To change the password the old one must be input
        if check_password(self.form['old_password'], verification.password):     # checks if the old pássword is right.

                                                                                            # If all requirements set above are met
            User.objects.filter(username=user).update(password=make_password(self.form['password1'])) # update the password to the new one.
            response = "continue"
            return response

        else:
            response = "invalid"
            return response # render the password change done page.
                                                        
