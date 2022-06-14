from django.contrib import admin
from .models import gallery, favorite, reports

# Register your models here.
admin.site.register(gallery)
admin.site.register(favorite)
admin.site.register(reports)
