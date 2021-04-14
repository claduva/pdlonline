from django.urls import path

from . import views

urlpatterns = [ 
    path("start_background_tasks/", views.start_background_tasks, name="start_backgorund_tasks"),
]