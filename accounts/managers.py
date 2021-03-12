from django.contrib.auth import models
from datetime import datetime
import string
import random

class DiscordUserManager(models.UserManager):
    def create_new_discord_user(self, user):
        new_user = self.create_user(
            username=user["username"],
            email=user["email"],
            discordid=user["id"], 
            avatar=user["avatar"], 
            public_flags=user["public_flags"], 
            flags=user["flags"], 
            locale=user["locale"], 
            mfa_enabled=user["mfa_enabled"], 
            discord_tag=f'{user["username"]}#{user["discriminator"]}',
        )
        return new_user
    
    def update_discord_user(self,found_user,user):
        placeholderusername=''.join(random.choices(string.ascii_uppercase + string.digits, k = 20)) 
        found_user.username=placeholderusername
        found_user.save()
        found_user.username=user["username"]
        found_user.discordid=user["id"], 
        found_user.avatar=user["avatar"]
        found_user.public_flags=user["public_flags"]
        found_user.flags=user["flags"]
        found_user.locale=user["locale"]
        found_user.mfa_enabled=user["mfa_enabled"]
        found_user.discord_tag=f'{user["username"]}#{user["discriminator"]}'
        found_user.save()
        return found_user