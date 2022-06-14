from django.urls import path
from . import views

urlpatterns = [
    path("TG2A", views.tg2a, name="TG2A"),
    path("TG2A/add", views.add_image, name="add_image"),
    path("gallery/<img_id>", views.image_page, name="image_page"),
    path("gallery_items/<page_num>", views.gallery_items, name="gallery_items"),
    path("TG2A/<user>", views.profile, name="profile"),
    path("report", views.report, name="report"),
    ]
