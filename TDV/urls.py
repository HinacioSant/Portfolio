from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path("TDV", views.tdv, name="tdv"),
    path("TDV/notes_page", views.notes_page, name="notes_page"),
    path("TDV/add_notes", views.add_notes, name="add_notes"),

    ]
