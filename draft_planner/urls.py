from django.urls import path

from . import views

urlpatterns = [ 
    path("draft_planner/", views.draft_planner, name="draft_planner"),
    path("draft_planner/save/", views.save_draft_plan, name="save_draft_plan"),
]