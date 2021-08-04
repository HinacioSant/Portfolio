from django.urls import path
from django.conf.urls import url
from . import views
from .tasks import scheduler

urlpatterns = [
    path("msa", views.msaindex, name="msa"),
    path("msa/menu/", views.msa_menu, name="msa_menu"),
    path("messages/<id1>/<id2>", views.messages, name="messages"),
    path("chat/<id1>/<id2>", views.chat, name="chat"),
    path("room_request", views.room_request, name="room_request"),
    path("search", views.search, name="search"),


]

scheduler.start() # Check tasks.py for more info
