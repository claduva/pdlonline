from django.db import models
from .managers import DiscordUserManager
import unicodedata
from django.utils.encoding import force_text

# Create your models here.

class DiscordUser(models.Model):
    objects = DiscordUserManager()

    id = models.BigIntegerField(primary_key=True)
    discord_tag = models.CharField(max_length=100)
    avatar = models.CharField(max_length=100)
    public_flags = models.IntegerField()
    flags = models.IntegerField()
    locale = models.CharField(max_length=100)
    mfa_enabled = models.BooleanField()
    last_login = models.DateTimeField(null=True)