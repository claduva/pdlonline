from django.urls import include, path
from rest_framework import routers
from django.views.decorators.csrf import csrf_exempt

from . import views

router = routers.DefaultRouter()
router.register(r'pokemon', views.PokemonViewSet,basename='pokemon')

urlpatterns = [ 
    path('api/', include(router.urls)),
    path('api/user/<int:discordid>/', views.UserLeagues,name="UserLeagues"),
    path('api/allabilities/', views.AllAbilities,name="AllAbilities"),
    path('api/allmoves/', views.AllMoves,name="AllMoves"),
    path('api/alltypes/', views.AllTypes,name="AllTypes"),
    path('api/league_pokemon/<int:id>/', views.LeaguePokemonDetail.as_view()),
    path('api/leagues/<int:id>/', views.LeagueDetail.as_view()),
    path('api/discord_settings/<int:subleague_id>/', views.DiscordSettingsDetail.as_view()),
]