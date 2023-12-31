
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("follow/", views.follow, name="follow"),
    path("following/<str:username>", views.following, name="following"),
    path("page/<int:pagenum>", views.make_pages, name="make_page"),
    path("like/<int:post>", views.like, name="like"),
    path("edit/", views.edit, name="edit")
]
