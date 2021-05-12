from django.urls import include, path
from rest_framework import routers
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [ 
    path('app_api/leagues/', views.LeagueList.as_view()),
]