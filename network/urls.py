
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("allPost", views.all_post, name="allpost"),
    path("newPost", views.new_post, name="newpost"),
    path("<str:username>", views.profile_page, name="profile"),
    path("follow/<int:id>/", views.follow, name="follow"),
    path("following/", views.following, name="following"),
    path("editpost/", views.editpost, name="editpost"),
    path("likeDislike/<int:id>", views.likeDislike, name="likeDislike")
]
