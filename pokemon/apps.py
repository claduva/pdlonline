from django.apps import AppConfig

class PokemonConfig(AppConfig):
    name = 'pokemon'

    def ready(self):
        import pokemon.signals