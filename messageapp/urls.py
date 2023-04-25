from django.urls import path
from . import views
from .tasks import scheduler

urlpatterns = [
    path("msa", views.msaindex, name="msa"),
    path("msa/menu/", views.msa_menu, name="msa_menu"),
    path("messages/<id1>/<id2>", views.messages, name="messages"),
    path("chat/<id1>/<id2>", views.chat, name="chat"),
    path("room_request", views.room_request, name="room_request"),
    path("check/<new_check>/", views.check, name="check"),
    path("msa/friend", views.friend, name="friend"),


]
# scheduler.start() # Check tasks.py for more info
