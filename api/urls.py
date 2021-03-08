from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'pokemon', views.PokemonViewSet,basename='pokemon')

urlpatterns = [ 
    path('api/', include(router.urls)),
]