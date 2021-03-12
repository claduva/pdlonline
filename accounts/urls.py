from django.urls import path

from . import views

urlpatterns = [ 
    path("discordlogin/", views.login_page, name="discordlogin"),
    path("oauth2-redirect", views.oauth2_redirect, name="discordredirect")
]