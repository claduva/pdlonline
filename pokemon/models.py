from django.db import models
from django.db.models import JSONField

# Create your models here.
class pokemon(models.Model):
    name = models.CharField(max_length=30,unique=True)
    pokedex_number = models.IntegerField(default=0)
    sprite = models.URLField(default="https://claduva.github.io/pdl_images/sprites/default.png")
    data=JSONField(null=True,blank=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        ordering = ['name']

class pokemon_basestats(models.Model):
    pokemon = models.OneToOneField(pokemon,on_delete=models.CASCADE,related_name='basestats')
    hp = models.IntegerField(default=0)
    attack = models.IntegerField(default=0)
    defense = models.IntegerField(default=0)
    special_attack = models.IntegerField(default=0)
    special_defense = models.IntegerField(default=0)
    speed = models.IntegerField(default=0)
    bst = models.IntegerField(default=0)

class pokemon_battlestats(models.Model):
    pokemon = models.OneToOneField(pokemon,on_delete=models.CASCADE,related_name='battlestats')
    kills = models.IntegerField(default=0)
    deaths = models.IntegerField(default=0)
    differential = models.IntegerField(default=0)
    gp = models.IntegerField(default=0)
    gw = models.IntegerField(default=0)
    support = models.IntegerField(default=0)
    damagedone = models.IntegerField(default=0)
    hphealed = models.IntegerField(default=0)
    luck = models.FloatField(default=0)
    remaininghealth = models.IntegerField(default=0)

class pokemon_type(models.Model):
    pokemon = models.ForeignKey(pokemon,on_delete=models.CASCADE,related_name='types')
    type = models.CharField(max_length=15)

    class Meta:
        unique_together = (("pokemon", "type"),)  

    def __str__(self):
        return f'Typing for {self.pokemon}'

class pokemon_ability(models.Model):
    pokemon = models.ForeignKey(pokemon,on_delete=models.CASCADE,related_name='abilities' )
    ability = models.CharField(max_length=30)

    class Meta:
        unique_together = (("pokemon", "ability"),)  

    def __str__(self):
        return f'Ability for {self.pokemon}'

class move(models.Model):
    name = models.CharField(max_length=50,unique=True)
    move_typing = models.CharField(max_length=10)
    move_category = models.CharField(max_length=10)
    move_power = models.IntegerField()
    move_accuracy = models.IntegerField()
    move_priority = models.IntegerField()
    move_crit_rate = models.DecimalField(max_digits=5, decimal_places=2,default=0.00)
    secondary_effect_chance = models.IntegerField()
    secondary_effect = models.CharField(max_length=100)
    
    def __str__(self):
        return f'Move data for {self.name}'

class pokemon_moveset(models.Model):
    pokemon = models.ForeignKey(pokemon,on_delete=models.CASCADE,related_name='moveset')
    move = models.ForeignKey(move,on_delete=models.CASCADE)

    class Meta:
        ordering = ['move__name']
        unique_together = (("pokemon", "move"),)  

    def __str__(self):
        return f'Moveset item for {self.pokemon}'

class pokemon_effectiveness(models.Model):
    pokemon = models.OneToOneField(pokemon,on_delete=models.CASCADE,related_name="effectiveness")
    bug=models.IntegerField(default=0)
    dark=models.IntegerField(default=0)
    dragon=models.IntegerField(default=0)
    electric=models.IntegerField(default=0)
    fairy=models.IntegerField(default=0)
    fighting=models.IntegerField(default=0)
    fire=models.IntegerField(default=0)
    flying=models.IntegerField(default=0)
    ghost=models.IntegerField(default=0)
    grass=models.IntegerField(default=0)
    ground=models.IntegerField(default=0)
    ice=models.IntegerField(default=0)
    normal=models.IntegerField(default=0)
    poison=models.IntegerField(default=0)
    psychic=models.IntegerField(default=0)
    rock=models.IntegerField(default=0)
    steel=models.IntegerField(default=0)
    water=models.IntegerField(default=0)