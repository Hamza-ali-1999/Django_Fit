from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("category", views.category, name="category"),
    path("wishlist", views.wishlist, name="wishlist"),
    path("listing/<int:id>", views.listing, name="listing"),
    path("listing/<int:id>/winner", views.winner, name="winner"),
    path("listing/<int:id>/bid", views.bid, name="bid"),
]
