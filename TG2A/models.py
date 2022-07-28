from django.db import models
from django.contrib.auth.models import User
from .validators import validate_file_size
from PIL import Image, ImageEnhance
from django.utils import timezone
import os

# Create your models here.
class gallery(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    image = models.ImageField(null=True, blank=True, upload_to="gallery_images/", validators=[validate_file_size])
    thumbnail_url = models.CharField(max_length=128, blank=True)
    date = models.DateTimeField(default=timezone.now, blank=True)


    def __str__(self):
        return 'Title: {} | Posted by {} at {}'.format(self.title, self.user, self.date.strftime('%d/%m/%Y %H:%M'))

    def test(self):
        Image.open(self.image)
        


    def get_thumbnail(self): # Get thumbnail method.
        size = (1920, 1080)
        image_name = "res.cloudinary.com/htmz79u9f/image/upload/v1/" + self.image.name
        print(image_name)
        image_thumbnail = "res.cloudinary.com/htmz79u9f/image/upload/v1/" + os.path.splitext(self.image.name)[0] + ".thumbnail"
        print(image_thumbnail)


        try:
            print("1")
            with Image.open(image_thumbnail): # If the thumbnail already exist
                print("2")

                return "/" + image_thumbnail  # return the url of it.

        except FileNotFoundError: # Else create one.
            print("11")
            with Image.open(image_name) as im:
                print("3")

                width, height = im.size
                gallery.objects.filter(id=self.id).update(thumbnail_url= "/" + image_thumbnail) # Add the url to the database.
                if im.mode in ("RGBA", "P"):
                     im = im.convert("RGB")

                if width < height: # If is a portait type image
                    print("4")

                    size = (1080,1080) # Different dimensions

                    if width < 1080: # Preventing image to be stretch out.
                        size = (1080,width)


                    im.thumbnail(size, Image.LANCZOS, reducing_gap=1.0)
                    im = ImageEnhance.Contrast(im)

                    im.enhance(1.3).save(image_thumbnail, "JPEG") # Add contrast and save.

                    return "/" + image_thumbnail # return the url.

                if height < 1080: # Preventing image to be stretch out.
                    print("5")

                    size = (1920,height)


                im.thumbnail(size, Image.LANCZOS, reducing_gap=1.0)
                im = ImageEnhance.Contrast(im)

                im.enhance(1.3).save(image_thumbnail, "JPEG") # Add contrast and save.

                return "/" + image_thumbnail # return url.


class favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ForeignKey(gallery, on_delete=models.CASCADE)
    favorite = models.BooleanField(default=False, null=True)

    def __str__(self):
        return '{} Favorited by {} | {}'.format(self.image.title, self.user, self.favorite)


class reports(models.Model):
    image_id = models.CharField(max_length=64)
    reason = models.CharField(max_length=64)
    more_info = models.CharField(max_length=64)

    def __str__(self):
        return '{} Reported for {}'.format(self.image_id, self.reason)
