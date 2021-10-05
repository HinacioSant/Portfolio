from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path("TG2A", views.tg2a, name="TG2A"),
    ]
