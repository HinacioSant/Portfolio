from .models import gallery, favorite
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .signals import my_callback
from django.utils import timezone
from datetime import datetime, timedelta


class image_management:
    def __init__(self, user, form):
        self.user = user
        self.form = form

    # Add image method
    def add_image(self):

        if self.form.is_valid(): # Check validity of the form.
            # Add image to the database.
            add = gallery(user= self.user, title=self.form['title'].value(), image=self.form['image'].value())

            # Limit one image upload per 3 sec window
            obj_check = gallery.objects.filter(user=self.user).last()
            if obj_check != None:
                last_created_obj = obj_check.date
                time_elapsed =  timezone.now() - last_created_obj
                if time_elapsed < timedelta(seconds=3):
                    return "ERROR: too many uploads in a small time window, wait before next upload."

            if len(gallery.objects.all()) >= 50:
                return "Gallery full!"

            if len(self.form['title'].value()) < 3:
                return "Title too short!(Titles must have at least 3 characters)"

            add.save()
            # Save and call get_thumbnail method. Check models.py for more info.
            add.get_thumbnail()

        else:
            return self.form.errors




    def fav(self, fav_form):
        # Variable added.
        check = favorite.objects.filter(user = self.user, image=self.form)

        # Check value of the variable.
        if fav_form == "favorite": # "favorite" means that the user is setting the object as a favorite.
            if not check: # If check variable comes back as a empty query set,
            # it means that the object wasn't created yet.
                # Create object.
                add = favorite(user = self.user, image=self.form, favorite=True)
                add.save()
            else: # If object already exist set favorite to true.
                check.update(favorite=True)

        else: # If the value of the variable is not "favorite", than the user is setting the object as a non-favorite.
            check.update(favorite=False)


    def check(self): # Check/return if the object is favorite or not.
        try:
            check = favorite.objects.get(user = self.user, image=self.form)
            if check.favorite == True: # Check if the object if favorite and return the response.
                response = "yes"
                return response
            else:
                response = "no"
                return response

        except ObjectDoesNotExist: # If object doesn't exist.
            response = "no" # Response is no.
            return response


    def delete_img(self):
        try:
            img_object = gallery.objects.get(id=self.form['image_id'], user=self.user)
            img_object.delete()

        except ObjectDoesNotExist:
            response = "Object does not exist!"
            return response


def infinite_scroll(gallery_content, page): # Infinite scroll function.
        lias = []
        for i in gallery_content:
            a = {"id":i.id, "thumbnail_url":i.thumbnail_url.url}
            lias.append(a)
        paginator = Paginator(lias, 20)

        try:
            items = paginator.page(page)

        except PageNotAnInteger:
            items = paginator.page(1)

        except EmptyPage:
            items = paginator.page(paginator.num_pages)


        # Check if there is more pages to load and return which.
        if items.has_next():
            page_num = items.next_page_number()
        else:
            page_num = ''

        response = {"items": items, "page_num": page_num}

        # The infinite scroll will only need to load a set of strings from the database,
        # and the template will load the images
        return response
