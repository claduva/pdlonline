from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import *

@receiver(post_save, sender=pokemon)
def create_new_pokemon(sender,instance,created,**kwargs):
    if created:
        pokemon_basestats.objects.create(pokemon=instance)
        pokemon_battlestats.objects.create(pokemon=instance)
        pokemon_effectiveness.objects.create(pokemon=instance)

@receiver(post_save, sender=pokemon)
def save_new_pokemon(sender, instance, **kwargs):
    instance.basestats.save()
    instance.battlestats.save()
    instance.effectiveness.save()