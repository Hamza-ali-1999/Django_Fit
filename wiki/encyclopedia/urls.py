from django.urls import path
from django import views
from.import views


urlpatterns = [
    
    path("", views.index, name="index"),
    path("wiki/<str:search>", views.wiki_search, name="wiki_search"),
    path("create_entry", views.create_entry, name="create_entry"),
    path("edit_entry/<str:title>", views.edit_entry, name="edit_entry")
]
