from django.urls import path

from . import views

urlpatterns = [ 
    path("", views.home, name="home"),
    path("leagues/", views.league_list, name="league_list"),
    path("discord/", views.discord, name="discord"),
    path("privacypolicy/", views.privacypolicy, name="privacypolicy"),
    path("settings/", views.settings, name="settings"),
    path("runscript/", views.runscript, name="runscript"),
    path("update_all_pokemon/", views.update_all_pokemon, name="update_all_pokemon"),
    path("old_database/", views.update_from_old_database, name="old_database"),
]