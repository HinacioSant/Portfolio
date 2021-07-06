from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path("msa", views.msaindex, name="msa"),
    path("msa/menu/", views.msa_menu, name="msa_menu"),

]
