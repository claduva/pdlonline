from django.db import models
from django.contrib.auth import get_user_model
UserModel = get_user_model()

# Create your models here.
class league(models.Model):
    name = models.CharField(max_length=50, unique=True)
    abbreviation = models.CharField(max_length=10)
    host = models.ForeignKey(UserModel,on_delete=models.CASCADE)
    moderators = models.ManyToManyField(UserModel,related_name="moderating")
    logo = models.URLField(max_length=400,default="https://media.discordapp.net/attachments/821585145961644062/821585187062153216/genericleague.png",blank=True)
    platform=models.CharField(max_length=30,choices=(
        ('Youtube Showdown','Youtube Showdown'),
        ('Youtube Wifi','Youtube Wifi'),
        ('Showdown','Showdown'),
        ('Wifi','Wifi'),
    ),default="Showdown")
    status=models.CharField(max_length=30,choices=(
        ('In Season','In Season'),
        ('Inactive','Inactive'),
        ('Recruiting Coaches','Recruiting Coaches'),
        ('In Offseason','In Offseason'),
    ),default="Inactive")
    discordserver=models.CharField(max_length=50, null=True,blank=True)
    discordurl=models.CharField(max_length=50, null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'League: {self.name}'

class league_configuration(models.Model):
    league = models.OneToOneField(league, on_delete=models.CASCADE,related_name="configuration")
    number_of_subleagues = models.IntegerField(default=1)
    allows_cross_subleague_matches = models.BooleanField(default=False)
    teambased = models.BooleanField(default=False)

    def __str__(self):
        return f'League configuration for {self.league.name}'

class subleague(models.Model):
    league = models.ForeignKey(league, on_delete=models.CASCADE,related_name="subleagues")
    name = models.CharField(max_length=30)

    def __str__(self):
        return f'{self.league.name} Subleague: {self.name}'