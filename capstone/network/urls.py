
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("update", views.update, name="update"),
    path("change_date", views.change_date, name="change_date"),
    path("create_workout", views.create_workout, name="create_workout"),
    path("explore", views.explore, name="explore"),
    path("saved_workouts", views.saved_workouts, name="saved_workouts"),

    #API Routes
    path("create_entry/<str:name>/<str:amount>/<int:value>/<str:date>", views.create_entry, name="create_entry"),
    path("remove_entry/<str:ID>/<str:date>", views.remove_entry, name="remove_entry"),
    path("update_meter/<str:date>", views.update_meter, name="update_meter"),
    path("workout_save/<str:ID>", views.workout_save, name="workout_save"),
    path("delete_workout/<str:ID>", views.delete_workout, name="delete_workout"),

]
