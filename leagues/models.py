from django.db import models
from django.contrib.auth import get_user_model
UserModel = get_user_model()
from league_configuration.models import league, subleague,conference,division,season

# Create your models here.
class application(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    league = models.ForeignKey(league, on_delete=models.CASCADE,related_name="applications")
    teamname = models.CharField(max_length=50)
    teamabbreviation = models.CharField(max_length=4)
    subleagues = models.ManyToManyField(subleague)
    alternate = models.BooleanField(default=False)
    showdown_username = models.CharField(max_length=50,null=True,blank=True)
    resume = models.TextField()
    replays = models.TextField(null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True)

class coach(models.Model):
    user = models.ManyToManyField(UserModel,related_name="coaching")
    season = models.ForeignKey(season, on_delete=models.CASCADE)
    teamname = models.CharField(max_length=50)
    teamabbreviation = models.CharField(max_length=4)
    logo = models.URLField(default="https://media.discordapp.net/attachments/821585145961644062/821585437163782154/genericteam.png",max_length=400,blank=True)
    conference = models.CharField(max_length=30)
    division = models.CharField(max_length=30, null=True, blank=True)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    forfeits = models.IntegerField(default=0)
    differential = models.IntegerField(default=0)
    streak = models.IntegerField(default=0)
    support = models.IntegerField(default=0)
    damagedone = models.IntegerField(default=0)
    hphealed = models.IntegerField(default=0)
    luck = models.FloatField(default=0)
    remaininghealth = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)