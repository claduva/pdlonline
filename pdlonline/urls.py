"""pdlonline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('', include('accounts.urls')),
    path('', include('api.urls')),
    path('', include('app_api.urls')),
    path('', include('backgroundtasks.urls')),
    path('',include("draft_planner.urls")),
    path('',include("league_configuration.urls")),
    path('',include("leagues.urls")),
    path('',include("main.urls")),
    path('',include("matches.urls")),
    path('',include("pokemon.urls")),

    ##unused
    #path('', include('django.contrib.auth.urls')),
]
