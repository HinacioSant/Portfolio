from django.urls import path

from . import views
# App Urls:
urlpatterns = [
    path("", views.index, name="index"),
    path("projects", views.projects, name="projects"),
    path("resume", views.resume, name="resume"),
    path("about", views.about, name="about"),
]
