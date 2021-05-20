from django.urls import path

from . import views

urlpatterns = [ 
    path("league/<int:league_id>/priorseason/<str:season_name>/", views.prior_season_home, name="prior_season"),
    path("league/<int:league_id>/priorseason/<str:season_name>/league_leaders/", views.prior_league_league_leaders, name="prior_total_league_leaders"),
    path("league/<int:league_id>/priorseason/<str:season_name>/subleague/<int:season_id>/", views.prior_subleague_home, name="prior_subleague_home"),
    path("league/<int:league_id>/priorseason/<str:season_name>/subleague/<int:season_id>/teams/<int:coach_id>/", views.prior_subleague_teampage, name="prior_teampage"),
    path("league/<int:league_id>/priorseason/<str:season_name>/subleague/<int:season_id>/draft/", views.prior_subleague_draft, name="prior_draft"),
    path("league/<int:league_id>/priorseason/<str:season_name>/subleague/<int:season_id>/free_agency/", views.prior_subleague_freeagency, name="prior_free_agency"),
    path("league/<int:league_id>/priorseason/<str:season_name>/subleague/<int:season_id>/trading/", views.prior_subleague_trading, name="prior_trading"),
    path("league/<int:league_id>/priorseason/<str:season_name>/subleague/<int:season_id>/schedule/", views.prior_subleague_schedule, name="prior_schedule"),
    path("league/<int:league_id>/priorseason/<str:season_name>/subleague/<int:season_id>/schedule/matchup/<int:match_id>/", views.prior_matchup, name="prior_matchup"),
    path("league/<int:league_id>/priorseason/<str:season_name>/subleague/<int:season_id>/schedule/replay/<int:match_id>/", views.prior_replay, name="prior_replay"),
    path("league/<int:league_id>/priorseason/<str:season_name>/subleague/<int:season_id>/league_leaders/", views.prior_subleague_league_leaders, name="prior_league_leaders"),
]