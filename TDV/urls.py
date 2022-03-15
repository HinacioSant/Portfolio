from django.urls import path
from . import views

urlpatterns = [
    path("TDV", views.tdv, name="tdv"),
    path("TDV/notes_page", views.notes_page, name="notes_page"),
    path("TDV/add_notes", views.add_notes, name="add_notes"),
    path("TDV/<note_id>/edit", views.edit_note, name="edit_note"),

    ]
