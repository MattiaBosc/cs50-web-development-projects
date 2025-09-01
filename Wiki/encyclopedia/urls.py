from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.title, name="search"),
    path("create", views.create, name="create"),
    path("random", views.random, name="random"),
    path("<str:title>", views.title, name="title")
]
