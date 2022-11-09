from django.urls import path

from encyclopedia import views

urlpatterns = [
    path("wiki/<str:title>", views.entry, name="entry"),
    path("create/", views.create, name="create"),
    path("search/", views.search, name="search"),
    path("random/", views.lucky, name="lucky"),
    path("wiki/<str:title>/edit/", views.edit, name="edit"),
    path("", views.index, name="index")
]
