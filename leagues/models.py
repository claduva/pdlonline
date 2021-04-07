from django.db import models
from django.contrib.auth import get_user_model
UserModel = get_user_model()
from league_configuration.models import league,subleague,conference,division,season,league_pokemon
from pokemon.models import pokemon

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

    def __str__(self):
        return f"{self.teamname} ({self.teamabbreviation}): {', '.join(list(self.user.all().values_list('username',flat=True)))}"

class roster(models.Model):
    team=models.ForeignKey(coach, on_delete=models.CASCADE,related_name="roster")
    pokemon=models.ForeignKey(pokemon, on_delete=models.CASCADE)
    gp = models.IntegerField(default=0)
    gw = models.IntegerField(default=0)
    kills = models.IntegerField(default=0)
    deaths = models.IntegerField(default=0)
    differential = models.IntegerField(default=0)
    streak = models.IntegerField(default=0)
    support = models.IntegerField(default=0)
    damagedone = models.IntegerField(default=0)
    hphealed = models.IntegerField(default=0)
    luck = models.FloatField(default=0)
    remaininghealth = models.IntegerField(default=0)

class draft(models.Model):
    team=models.ForeignKey(coach, on_delete=models.CASCADE,related_name="draft")
    pokemon=models.ForeignKey(pokemon, on_delete=models.CASCADE, null=True)
    picknumber=models.IntegerField()
    points=models.IntegerField(null=True)
    picktime=models.DateTimeField(auto_now=True, null=True)
    skipped=models.BooleanField(default=False)
    announced=models.BooleanField(default=False)

class left_pick(models.Model):
    team=models.ForeignKey(coach, on_delete=models.CASCADE)
    pokemon=models.ForeignKey(pokemon, on_delete=models.CASCADE, null=True)

class free_agency(models.Model):
    team=models.ForeignKey(coach, on_delete=models.CASCADE)
    dropped_pokemon=models.ForeignKey(pokemon, on_delete=models.CASCADE, null=True,related_name="fa_dropped")
    added_pokemon=models.ForeignKey(pokemon, on_delete=models.CASCADE, null=True,related_name="fa_added")
    timeeffective=models.DateTimeField()
    created=models.DateTimeField(auto_now_add=True)
    executed=models.BooleanField(default=False)
    announced=models.BooleanField(default=False)

class trading(models.Model):
    team=models.ForeignKey(coach, on_delete=models.CASCADE)
    dropped_pokemon=models.ForeignKey(pokemon, on_delete=models.CASCADE, null=True,related_name="trade_dropped")
    added_pokemon=models.ForeignKey(pokemon, on_delete=models.CASCADE, null=True,related_name="trade_added")
    timeeffective=models.DateTimeField()
    created=models.DateTimeField(auto_now_add=True)
    executed=models.BooleanField(default=False)
    announced=models.BooleanField(default=False)

class trade_request(models.Model):
    offeredpokemon=models.ForeignKey(roster,on_delete=models.CASCADE,related_name="offered")
    requestedpokemon=models.ForeignKey(roster,on_delete=models.CASCADE,related_name="requested")
    sent=models.BooleanField(default=False)

class match(models.Model):
    week=models.IntegerField(null=True,blank=True)
    playoff_week=models.CharField(max_length=30,null=True,blank=True)
    duedate=models.DateTimeField(null=True)
    team1 = models.ForeignKey(coach,on_delete=models.CASCADE, related_name="team1")
    team2 = models.ForeignKey(coach,on_delete=models.CASCADE, related_name="team2")
    winner = models.ForeignKey(coach,on_delete=models.CASCADE, related_name="winner",null=True)
    team1score = models.IntegerField(default=0)
    team2score = models.IntegerField(default=0)
    replay = models.CharField(max_length=200,null=True)
    data=models.JSONField(null=True)
    timestamp= models.DateTimeField(auto_now=True)
    announced = models.BooleanField(default=False)