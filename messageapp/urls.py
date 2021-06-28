from django.urls import path
from . import views

urlpatterns = [
    path("msa", views.msaindex, name="msa"),

]
