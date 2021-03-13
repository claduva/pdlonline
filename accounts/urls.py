from django.urls import path

from . import views

urlpatterns = [ 
    path("discordlogin/", views.login_page, name="discordlogin"),
    path("logout", views.logout_user, name="logout"),
    path("oauth2-redirect", views.oauth2_redirect, name="discordredirect"),
]