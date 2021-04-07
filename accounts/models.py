from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser
from .managers import DiscordUserManager

class CustomUser(AbstractUser):
    discordid = models.BigIntegerField(unique=True)
    discord_tag = models.CharField(max_length=100,null=True)
    avatar = models.CharField(max_length=100,null=True)
    public_flags = models.IntegerField(null=True)
    flags = models.IntegerField(null=True)
    locale = models.CharField(max_length=100,null=True)
    mfa_enabled = models.BooleanField(null=True)

    objects = DiscordUserManager()
    
    class Meta:
        ordering = ['username']

    def __str__(self):
        return self.username