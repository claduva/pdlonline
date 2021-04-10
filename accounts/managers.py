from django.contrib.auth import models
from datetime import datetime
import string
import random

class DiscordUserManager(models.UserManager):
    def create_new_discord_user(self, user):
        new_user = self.create_user(
            username=f'{user["username"]}#{user["discriminator"]}',
            email=user["email"],
            discordid=user["id"], 
            avatar=user["avatar"], 
            public_flags=user["public_flags"], 
            flags=user["flags"], 
            locale=user["locale"], 
            mfa_enabled=user["mfa_enabled"], 
            discord_tag=f'{user["username"]}#{user["discriminator"]}',
            showdown_alts="[]"
        )
        return new_user
