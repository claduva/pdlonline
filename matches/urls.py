from django.urls import path

from . import views

urlpatterns = [ 
    path("replay_analyzer/", views.replay_analyzer, name="replay_analyzer"),
]