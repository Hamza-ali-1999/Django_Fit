
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_view, name="create"),
    path("profile/<int:ID>", views.profile, name="profile"),
    path("following", views.following, name="following"),

    path("edit_post/<int:ID>/<str:new_text>", views.edit_post ,name="edit_post"),

    #API Routes (Some used for testing and learning)
    path("posts/<str:postbox>/<int:page_number>", views.postbox, name="postbox"),
    path("list/<int:ID>", views.following_list, name="following_list"),
    path("logged_user", views.logged_user, name="logged_user"),
    path("like_post/<int:ID>", views.like_post ,name="like_post"),
    path("follow_user/<int:ID>", views.follow_user ,name="follow_user"),
    
]
