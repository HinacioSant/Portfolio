from django.urls import path, re_path
from django.conf.urls import include
from django.contrib.auth import views as auth_views

from . import views
# App Urls:
urlpatterns = [
    path("home", views.home, name="home"),
    path("login", views.login, name="login"),
    path("register", views.register, name="register"),
    path("logout", views.logout, name="logout"),
    path("lg", views.lg, name="lg"),
    path("password_change", views.password_change, name="password_change"),
    re_path(r'^oauth/', include('social_django.urls', namespace='social')),

    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="recover/password_reset.html"), name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="recover/password_reset_sent.html"), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="recover/password_reset_form.html"), name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="recover/password_reset_done.html"), name="password_reset_complete"),

    ]
