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
        return 'Title: {} | Posted by {} at {}'.format(self.title, self.user, self.date)


    def get_thumbnail(self): # Get thumbnail method.
        size = (720, 405)
        image_name = "media/" + self.image.name
        image_thumbnail = "media/" + os.path.splitext(self.image.name)[0] + ".thumbnail"


        try:
            with Image.open(image_thumbnail): # If the thumbnail already exist
                return "/" + image_thumbnail  # return the url of it.

        except FileNotFoundError: # Else create one.
            with Image.open(image_name) as im:
                width, height = im.size
                gallery.objects.filter(id=self.id).update(thumbnail_url= "/" + image_thumbnail) # Add the url to the database.
                if width < height: # If is a portait type image
                    size = (607,867) # Different dimensions
                    im.thumbnail(size, Image.LANCZOS, reducing_gap=1.0)
                    im = ImageEnhance.Contrast(im)


                    im.enhance(1.3).save(image_thumbnail, "JPEG") # Add contrast and save.

                    return "/" + image_thumbnail # return the url.

                im.thumbnail(size, Image.LANCZOS, reducing_gap=1.0)
                im = ImageEnhance.Contrast(im)


                im.enhance(1.3).save(image_thumbnail, "JPEG") # Add contrast and save.

                return "/" + image_thumbnail # return url.


class favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ForeignKey(gallery, on_delete=models.CASCADE)
    favorite = models.BooleanField(default=False, null=True)

    def __str__(self):
        return 'Is this item favorite by user: {} | {}'.format(self.user, self.favorite)
