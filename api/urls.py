from django.urls import include, path
from rest_framework import routers
from django.views.decorators.csrf import csrf_exempt

from . import views

router = routers.DefaultRouter()
router.register(r'pokemon', views.PokemonViewSet,basename='pokemon')
router.register(r'bot_message', views.BotMessageViewSet,basename='bot_message')

urlpatterns = [ 
    path('api/', include(router.urls)),
    path('api/user/<int:discordid>/', views.UserLeagues,name="UserLeagues"),
    path('api/allabilities/', views.AllAbilities,name="AllAbilities"),
    path('api/allmoves/', views.AllMoves,name="AllMoves"),
    path('api/alltypes/', views.AllTypes,name="AllTypes"),
    path('api/league_pokemon/<int:id>/', views.LeaguePokemonDetail.as_view()),
    path('api/leagues/<int:id>/', views.LeagueDetail.as_view()),
    path('api/discord_settings/<int:subleague_id>/', views.DiscordSettingsDetail.as_view()),
    path('api/draft/', views.DraftList.as_view()),
    path('api/draft/<int:pk>/', views.DraftDetail.as_view()),
    path('api/draft/', views.DraftList.as_view()),
    path('api/draft/<int:pk>/', views.DraftDetail.as_view()),
    path('api/draft/nextpick/<int:subleague_id>/<int:picknumber>/', views.nextpick),
    path('api/free_agency/', views.FreeAgencyList.as_view()),
    path('api/free_agency/<int:pk>/', views.FreeAgencyDetail.as_view()),
    path('api/trading/', views.TradingList.as_view()),
    path('api/trading/<int:pk>/', views.TradingDetail.as_view()),
]