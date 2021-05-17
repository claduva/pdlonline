from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser
from .managers import DiscordUserManager
from timezone_field import TimeZoneField
from django.contrib.postgres.fields import ArrayField

class CustomUser(AbstractUser):
    discordid = models.BigIntegerField(unique=True,null=True)
    discord_tag = models.CharField(max_length=100,null=True)
    avatar = models.CharField(max_length=100,null=True)
    public_flags = models.IntegerField(null=True)
    flags = models.IntegerField(null=True)
    locale = models.CharField(max_length=100,null=True)
    mfa_enabled = models.BooleanField(null=True)
    biography = models.TextField(null=True,blank=True)
    timezone = models.CharField(max_length=100,null=True,blank=True)
    showdown_alts=ArrayField(models.CharField(max_length=30, blank=True,null=True),null=True)

    objects = DiscordUserManager()
    
    class Meta:
        ordering = ['username']

    def __str__(self):
        return self.username
