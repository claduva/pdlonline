from django.urls import path

from . import views

urlpatterns = [ 
    path("league/<int:league_id>/apply/", views.apply, name="apply"),
    path("league/<int:league_id>/", views.league_home, name="league_home"),
    path("league/<int:league_id>/subleague/<int:subleague_id>/", views.subleague_home, name="subleague_home"),
]