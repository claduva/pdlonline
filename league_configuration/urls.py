from django.urls import path

from . import views

urlpatterns = [ 
    path("create_league/", views.create_league, name="create_league"),
    path("settings/leagues_moderating/", views.leagues_moderating, name="leagues_moderating"),
    path("settings/leagues_moderating/<int:league_id>/", views.league_settings, name="league_settings"),
    path("settings/leagues_moderating/<int:league_id>/configuration/", views.league_configuration, name="league_configuration"),
    path("settings/leagues_moderating/<int:league_id>/configuration/<int:subleague_id>/", views.subleague_configuration, name="subleague_configuration"),
    path("settings/leagues_moderating/<int:league_id>/configuration/<int:subleague_id>/delete/", views.delete_subleague, name="delete_subleague"),
]