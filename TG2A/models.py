from django.db import models
from django.contrib.auth.models import User
from .validators import validate_file_size
from PIL import Image, ImageEnhance
import os

# Create your models here.
class gallery(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    image = models.ImageField(null=True, blank=True, upload_to="gallery_images/", validators=[validate_file_size])


    def __str__(self):
        return 'Title: {} | Posted by {}'.format(self.title, self.user)


    def get_thumbnail(self):
        size = (720, 405)
        image_name = "media/" + self.image.name
        image_thumbnail = "media/" + os.path.splitext(self.image.name)[0] + ".thumbnail"


        try:
            with Image.open(image_thumbnail):
                return "/" + image_thumbnail

        except FileNotFoundError:
            with Image.open(image_name) as im:
                width, height = im.size
                if width < height:                    
                    size = (607,867)
                    im.thumbnail(size, Image.LANCZOS, reducing_gap=1.0)
                    im = ImageEnhance.Contrast(im)


                    im.enhance(1.3).save(image_thumbnail, "JPEG")

                    return "/" + image_thumbnail

                im.thumbnail(size, Image.LANCZOS, reducing_gap=1.0)
                im = ImageEnhance.Contrast(im)


                im.enhance(1.3).save(image_thumbnail, "JPEG")

                return "/" + image_thumbnail
