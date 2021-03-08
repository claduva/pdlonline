from django.urls import path

from . import views

urlpatterns = [ 
    path("pokedex/", views.pokedex, name="pokedex"),
    path("pokedex/<str:pokemon_item>/", views.pokedex_entry, name="pokedex_entry"),
]