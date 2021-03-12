from django.contrib.auth.backends import BaseBackend
from .models import DiscordUser
from django.contrib.auth.models import User

class DiscordAuthenticationBackend(BaseBackend):
    def authenticate(self, request, user) -> DiscordUser:
        try:
            found_user = DiscordUser.objects.get(id=user["id"])
            found_user = DiscordUser.objects.update_discord_user(found_user,user)
            print("User found.")
            return found_user
        except:
            print("User not found.")
            new_user = DiscordUser.objects.create_new_discord_user(user)
            return new_user

        