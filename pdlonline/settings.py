"""
Django settings for pdlonline project.

Generated by 'django-admin startproject' using Django 2.2.10.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import sys
import socket

if (socket.gethostname().find("local")>-1 or socket.gethostname().find("Harshith")>-1):
    DEBUG = True
    from .configuration import *
    SECRET_KEY = SECRET_KEY
    NAME=NAME
    USER=USER
    PASSWORD=PASSWORD
    HOST=HOST
    ROOTURL="https://pokemondraftleagueonline.herokuapp.com"
else:
    DEBUG = True
    SECRET_KEY = os.environ.get('SECRET_KEY','developmentkey')
    NAME=os.environ.get('NAME')
    USER=os.environ.get('USER')
    PASSWORD=os.environ.get('PASSWORD')
    HOST=os.environ.get('HOST')
    ROOTURL="https://pokemondraftleagueonline.herokuapp.com"

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ALLOWED_HOSTS = ['0.0.0.0','127.0.0.1','localhost','pokemondraftleagueonline.herokuapp.com']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.postgres',
    'django.contrib.staticfiles',

    #local apps
    'accounts.apps.AccountsConfig',
    'api.apps.ApiConfig',
    'draft_planner.apps.DraftPlannerConfig',
    'league_configuration.apps.LeagueConfigurationConfig',
    'leagues.apps.LeaguesConfig',
    'main.apps.MainConfig',
    'matches.apps.MatchesConfig',
    'pokemon.apps.PokemonConfig',
    
    #third party apps
    'background_task',
    'crispy_forms',
    'django_bootstrap_breadcrumbs',
    'rest_framework',
    'multiselectfield',
    'template_timings_panel',
    'storages',
    'timezone_field',
    'widget_tweaks',

    #autoregister
    'admin_autoregister',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    #third-party middleware
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'pdlonline.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,"templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'pdlonline.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': NAME,                      
        'USER': USER,
        'PASSWORD': PASSWORD,
        'HOST': HOST,
        'PORT': '5432',
        'TEST': {
          'NAME': 'testdb',
        }
    },
}

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, 'pdlonline/staticfiles')
STATIC_URL = '/static/' 
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


#other settings
LOGIN_REDIRECT_URL = 'home'
LOGIN_URL = 'discordlogin'
LOGOUT_REDIRECT_URL = 'home'

AUTH_USER_MODEL = 'accounts.CustomUser'

AUTHENTICATION_BACKENDS = [
    'accounts.auth.DiscordAuthenticationBackend',
    'django.contrib.auth.backends.ModelBackend',
]

CRISPY_TEMPLATE_PACK = 'bootstrap4'
BREADCRUMBS_TEMPLATE = "django_bootstrap_breadcrumbs/bootstrap4.html"

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
            'rest_framework.renderers.JSONRenderer',
    ),
    }
