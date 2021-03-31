from django.urls import path

from . import views

urlpatterns = [ 
    path("create_league/", views.create_league, name="create_league"),
    path("settings/leagues_moderating/", views.leagues_moderating, name="leagues_moderating"),
    path("settings/leagues_moderating/<int:league_id>/", views.league_settings, name="league_settings"),
    path("settings/leagues_moderating/<int:league_id>/configuration/", views.league_configuration, name="league_configuration"),
    path("settings/leagues_moderating/<int:league_id>/configuration/<int:subleague_id>/", views.subleague_configuration, name="subleague_configuration"),
    path("settings/leagues_moderating/<int:league_id>/configuration/<int:subleague_id>/season/", views.season_configuration, name="season_configuration"),
    path("settings/leagues_moderating/<int:league_id>/configuration/<int:subleague_id>/delete/", views.delete_subleague, name="delete_subleague"),
    path("settings/leagues_moderating/<int:league_id>/configuration/<int:subleague_id>/conferences_and_divisions/", views.subleague_conferences_and_divisions, name="conferences_and_divisions"),
       path("settings/leagues_moderating/<int:league_id>/configuration/<int:subleague_id>/conferences_and_divisions/<int:conference_id>/add_division/", views.add_division, name="add_division"),
    path("settings/leagues_moderating/<int:league_id>/configuration/<int:subleague_id>/conferences_and_divisions/<int:conference_id>/delete/", views.delete_conference, name="delete_conference"),
    path("settings/leagues_moderating/<int:league_id>/configuration/<int:subleague_id>/conferences_and_divisions/<int:conference_id>/<int:division_id>/delete/", views.delete_division, name="delete_division"),
    path("settings/leagues_moderating/<int:league_id>/configuration/<int:subleague_id>/rules/", views.subleague_rules, name="subleague_rules"),
    path("settings/leagues_moderating/<int:league_id>/configuration/<int:subleague_id>/manage_tiers/", views.manage_tiers, name="manage_tiers"),
    path("settings/leagues_moderating/<int:league_id>/configuration/<int:subleague_id>/manage_tiers/tiers_from_scratch/", views.tiers_from_scratch, name="tiers_from_scratch"),
    path("settings/leagues_moderating/<int:league_id>/configuration/<int:subleague_id>/manage_tiers/upload_tiers_csv/", views.upload_tiers_csv, name="upload_tiers_csv"),
    path("settings/leagues_moderating/<int:league_id>/configuration/<int:subleague_id>/manage_tiers/tiers_site_template/", views.tiers_site_template, name="tiers_site_template"),
    path("settings/leagues_moderating/<int:league_id>/configuration/<int:subleague_id>/manage_tiers/tiers_other_league/", views.tiers_other_league, name="tiers_other_league"),
    path("settings/leagues_moderating/<int:league_id>/configuration/<int:subleague_id>/manage_tiers/edit_tier/<int:tier_id>/", views.edit_tier, name="edit_tier"),
    path("settings/leagues_moderating/<int:league_id>/configuration/<int:subleague_id>/manage_tiers/delete_tier/<int:tier_id>/", views.delete_tier, name="delete_tier"),
]