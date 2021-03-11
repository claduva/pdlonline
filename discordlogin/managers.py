from django.contrib.auth import models

class DiscordUserManager(models.UserManager):
    def create_new_discord_user(self, user):
        new_user = self.create_user(
            id=user["id"], 
            avatar=user["avatar"], 
            public_flags=user["public_flags"], 
            flags=user["flags"], 
            locale=user["locale"], 
            mfa_enabled=user["mfa_enabled"], 
            discord_tag=f'{user["username"]}#{user["discriminator"]}'
        )
        return new_user