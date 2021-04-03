from django.urls import path

from . import views

urlpatterns = [ 
    path("league/<int:league_id>/apply/", views.apply, name="apply"),
    path("league/<int:league_id>/", views.league_home, name="league_home"),
    path("league/<int:league_id>/subleague/<int:subleague_id>/", views.subleague_home, name="subleague_home"),
    path("league/<int:league_id>/subleague/<int:subleague_id>/tiers/", views.subleague_tierset, name="tiers"),
    path("league/<int:league_id>/subleague/<int:subleague_id>/draft/", views.subleague_draft, name="draft"),
    path("league/<int:league_id>/subleague/<int:subleague_id>/draft/execute_draft/", views.execute_draft, name="execute_draft"),
    path("league/<int:league_id>/subleague/<int:subleague_id>/draft/skip/", views.skip_pick, name="skip_pick"),
    path("league/<int:league_id>/subleague/<int:subleague_id>/draft/leave_pick/", views.leave_pick, name="leave_pick"),
    path("league/<int:league_id>/subleague/<int:subleague_id>/draft/delete_pick/<int:pick_id>/", views.delete_left_pick, name="delete_left_pick"),
    path("league/<int:league_id>/subleague/<int:subleague_id>/rules/", views.subleague_ruleset, name="rules"),
]