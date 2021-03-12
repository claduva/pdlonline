from django.contrib.auth import models
from datetime import datetime

class DiscordUserManager(models.UserManager):
    def create_new_discord_user(self, user):
        new_user = self.create(
            id=user["id"], 
            email=user["email"],
            avatar=user["avatar"], 
            public_flags=user["public_flags"], 
            flags=user["flags"], 
            locale=user["locale"], 
            mfa_enabled=user["mfa_enabled"], 
            discord_tag=f'{user["username"]}#{user["discriminator"]}',
            last_login=datetime.now()
        )
        return new_user
    
    def update_discord_user(self,found_user,user):
        found_user.email=user["email"]
        found_user.avatar=user["avatar"]
        found_user.public_flags=user["public_flags"]
        found_user.flags=user["flags"]
        found_user.locale=user["locale"]
        found_user.mfa_enabled=user["mfa_enabled"]
        found_user.discord_tag=f'{user["username"]}#{user["discriminator"]}'
        found_user.last_login=datetime.now()
        found_user.save()
        return found_user