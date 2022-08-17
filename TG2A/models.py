from django.db import models
from django.core.files.base import ContentFile
from django.contrib.auth.models import User
from .validators import validate_file_size
from PIL import Image, ImageEnhance
from django.utils import timezone
import os
from io import BytesIO
# Create your models here.
class gallery(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    image = models.ImageField(null=True, blank=True, upload_to="gallery_images/", validators=[validate_file_size])
    thumbnail_url = models.ImageField(null=True, blank=True, upload_to="gallery_images/", validators=[validate_file_size])
    date = models.DateTimeField(default=timezone.now, blank=True)


    def __str__(self):
        return 'Title: {} | Posted by {} at {}'.format(self.title, self.user, self.date.strftime('%d/%m/%Y %H:%M'))

    def get_url(self):
        return "1"

    def get_thumbnail(self): # Get thumbnail method.
        size = (1920, 1080)
        image_name = self.image



        with Image.open(image_name) as im:

            width, height = im.size
            if im.mode in ("RGBA", "P"):
                 im = im.convert("RGB")

            if width < height: # If is a portait type image

                size = (1080,1080) # Different dimensions

                if width < 1080: # Preventing image to be stretch out.
                    size = (1080,width)


                im.thumbnail(size, Image.LANCZOS, reducing_gap=1.0)
                im = ImageEnhance.Contrast(im)

                t = BytesIO()
                im.enhance(1.3).save(t, "JPEG")
                t.seek(0)
                self.thumbnail_url.save("thumb", ContentFile(t.read()))
                t.close()


                return "200"
            if height < 1080: # Preventing image to be stretch out.

                size = (1920,height)


            im.thumbnail(size, Image.LANCZOS, reducing_gap=1.0)
            im = ImageEnhance.Contrast(im)

            t = BytesIO()
            im.enhance(1.3).save(t, "JPEG")
            t.seek(0)
            self.thumbnail_url.save("thumb", ContentFile(t.read()))
            t.close()
            return "200"

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
