from django.db import models
from django.contrib.auth import get_user_model
UserModel = get_user_model()

from pokemon.models import pokemon

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

class discord_settings(models.Model):
    subleague = models.OneToOneField(subleague, on_delete=models.CASCADE)
    server=models.BigIntegerField(null=True)
    draftchannel=models.BigIntegerField(null=True)
    replaychannel=models.BigIntegerField(null=True)
    fachannel=models.BigIntegerField(null=True)
    tradechannel=models.BigIntegerField(null=True)
    
class league_tier(models.Model):
    subleague = models.ForeignKey(subleague, on_delete=models.CASCADE,related_name="tiers")
    tier = models.CharField(max_length=20)
    points = models.IntegerField(null=True)
    
    class Meta:
        unique_together = (("subleague", "tier"),) 
        ordering = ['-points']

class league_pokemon(models.Model):
    subleague = models.ForeignKey(subleague, on_delete=models.CASCADE,related_name="pokemon_list")
    pokemon = models.ForeignKey(pokemon, on_delete=models.CASCADE)
    tier = models.ForeignKey(league_tier, on_delete=models.CASCADE)
    team = models.CharField(max_length=40,null=True)

    class Meta:
        unique_together = (("subleague", "pokemon"),) 

    def __str__(self):
        return f'{self.subleague.league.name}-{self.subleague.name}: {self.pokemon.name}'

class tier_template(models.Model):
    name = models.CharField(max_length=20)
    pokemon = models.ForeignKey(pokemon, on_delete=models.CASCADE)
    tier = models.CharField(max_length=20)
    points = models.IntegerField(null=True)

class conference(models.Model):
    subleague = models.ForeignKey(subleague, on_delete=models.CASCADE, related_name="conferences")
    conference = models.CharField(max_length=40)

class division(models.Model):
    subleague = models.ForeignKey(subleague, on_delete=models.CASCADE,related_name="divisions")
    division = models.CharField(max_length=40)

class rules(models.Model):
    subleague = models.OneToOneField(subleague, on_delete=models.CASCADE)
    rules = models.TextField(default="No rules entered")


class season(models.Model):
    league = models.ForeignKey(league, on_delete=models.CASCADE)
    subleague = models.ForeignKey(subleague, on_delete=models.SET_NULL,related_name='seasons',null=True)
    subleague_name = models.CharField(max_length=30,null=True)
    name = models.CharField(max_length=20)
    draftstart=models.DateTimeField(null=True,blank=True)
    drafttimer=models.IntegerField(default=12)
    draftbudget = models.IntegerField(default=1000)
    picksperteam = models.IntegerField(default=11)
    drafttype = models.CharField(max_length=25, choices=(("Snake","Snake"),("Auction","Auction")),default="Snake")
    seasonstart=models.DateTimeField(null=True,blank=True)
    seasonlength = models.IntegerField(default=7)
    playoffslength = models.IntegerField(default=3)
    freeagenciesallowed= models.IntegerField(default=4)
    tradesallowed= models.IntegerField(default=4)
    created = models.DateTimeField(auto_now_add=True)
    archived = models.BooleanField(default=False)

    class Meta:
        ordering = ['created']