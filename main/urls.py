from django.urls import path

from . import views

urlpatterns = [ 
    path("", views.home, name="home"),
    path("runscript/", views.runscript, name="runscript"),
    path("update_all_pokemon/", views.update_all_pokemon, name="update_all_pokemon"),
    path("old_database/", views.update_from_old_database, name="old_database"),
]