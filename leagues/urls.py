from django.urls import path

from . import views

urlpatterns = [ 
    path("league/<int:league_id>/apply/", views.apply, name="apply"),
    path("league/<int:league_id>/", views.league_home, name="league_home"),
    path("league/<int:league_id>/subleague/<int:subleague_id>/", views.subleague_home, name="subleague_home"),
    path("league/<int:league_id>/subleague/<int:subleague_id>/teams/<int:coach_id>/", views.subleague_teampage, name="teampage"),
    path("league/<int:league_id>/subleague/<int:subleague_id>/tiers/", views.subleague_tierset, name="tiers"),
    path("league/<int:league_id>/subleague/<int:subleague_id>/draft/", views.subleague_draft, name="draft"),
    path("league/<int:league_id>/subleague/<int:subleague_id>/draft/execute_draft/", views.execute_draft, name="execute_draft"),
    path("league/<int:league_id>/subleague/<int:subleague_id>/draft/make_up_pick/", views.make_up_pick, name="make_up_pick"),
    path("league/<int:league_id>/subleague/<int:subleague_id>/draft/skip/", views.skip_pick, name="skip_pick"),
    path("league/<int:league_id>/subleague/<int:subleague_id>/draft/leave_pick/", views.leave_pick, name="leave_pick"),
    path("league/<int:league_id>/subleague/<int:subleague_id>/draft/delete_pick/<int:pick_id>/", views.delete_left_pick, name="delete_left_pick"),
    path("league/<int:league_id>/subleague/<int:subleague_id>/free_agency/", views.subleague_freeagency, name="free_agency"),
    path("league/<int:league_id>/subleague/<int:subleague_id>/trading/", views.subleague_trading, name="trading"),
    path("league/<int:league_id>/subleague/<int:subleague_id>/trading/actions/", views.trading_actions, name="trading_actions"),
    path("league/<int:league_id>/subleague/<int:subleague_id>/schedule/", views.subleague_schedule, name="schedule"),
    path("league/<int:league_id>/subleague/<int:subleague_id>/schedule/forfeits/<int:match_id>/", views.handle_forfeits, name="handle_forfeits"),
    path("league/<int:league_id>/subleague/<int:subleague_id>/schedule/matchup/<int:match_id>/", views.matchup, name="matchup"),
    path("league/<int:league_id>/subleague/<int:subleague_id>/schedule/upload_replay/<int:match_id>/", views.upload_replay, name="upload_replay"),
    path("league/<int:league_id>/subleague/<int:subleague_id>/schedule/replay/<int:match_id>/", views.replay, name="replay"),
    path("league/<int:league_id>/subleague/<int:subleague_id>/league_leaders/", views.subleague_league_leaders, name="league_leaders"),
    path("league/<int:league_id>/subleague/<int:subleague_id>/rules/", views.subleague_ruleset, name="rules"),
]