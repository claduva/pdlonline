import json
import _jsonnet
import requests
from django.core.management.base import BaseCommand
from pokemon.models import pokemon


class Command(BaseCommand):
    help = 'Populates the pokemon table'

    def handle(self, *args, **options):

        # Using https://github.com/itsjavi/showdown-data might be worth to remove this weird
        # jsonnet dependency.

        pokedex_response = requests.get('https://play.pokemonshowdown.com/data/pokedex.js')
        pokedex = json.loads(_jsonnet.evaluate_snippet('snippet', pokedex_response.text.split(' = ', 1)[1][:-1]))
        pokedex = {k: v for k, v in pokedex.items() if is_valid_pokemon(k, v)}

        typechart_response = requests.get('https://play.pokemonshowdown.com/data/typechart.js')
        typechart = json.loads(_jsonnet.evaluate_snippet('snippet', typechart_response.text.split(' = ', 1)[1][:-1]))
        
        learnsets_response = requests.get('https://play.pokemonshowdown.com/data/learnsets.js')
        learnsets = json.loads(_jsonnet.evaluate_snippet('snippet', learnsets_response.text.split(' = ', 1)[1][:-1]))

        moves_response = requests.get('https://play.pokemonshowdown.com/data/moves.js')
        moves = json.loads(_jsonnet.evaluate_snippet('snippet', moves_response.text.replace('self:', 'self_:').split(' = ', 1)[1][:-1]))

        pokemon_objects = []
        for poke_identifier, poke_data in pokedex.items():
            name = poke_data['name'].replace('’', "'").replace(': ', ":").replace('é', 'e')

            basestats = {
                'hp': poke_data['baseStats']['hp'],
                'attack': poke_data['baseStats']['atk'],
                'defense': poke_data['baseStats']['def'],
                'special_attack': poke_data['baseStats']['spa'],
                'special_defense': poke_data['baseStats']['spd'],
                'speed': poke_data['baseStats']['spe']
            }
            basestats['bst'] = sum(basestats.values())

            data = {
                'id': poke_data['num'],
                'types': poke_data['types'],
                'pokemon': name,
                'movesets': calculate_moveset(poke_identifier, poke_data, pokedex, moves, learnsets),
                'abilities': list(poke_data['abilities'].values()),
                'basestats': basestats,
                'type_effectiveness': calculate_type_effectiveness(poke_data['types'], typechart),
            }

            pokemon_objects.append(pokemon(name=name, pokedex_number=poke_data['num'], sprite=validate_sprite(name), data=data))

        pokemon.objects.bulk_create(pokemon_objects)


def validate_sprite(name):

    sanitized_name = name.lower().replace('mega-', 'mega').replace("'", "").replace('o-o', 'oo').replace('.', '').replace(' ', '') \
        .replace('dusk-', 'dusk').replace('dawn-', 'dawn').replace('rapid-', 'rapid').replace('%', '').replace(':', '')

    potential_sprite = 'https://claduva.github.io/pdl_images/sprites/dex/ani/standard/' + sanitized_name + '.gif'
    if requests.get(potential_sprite).status_code == 200:
        return potential_sprite

    print('no gif found for ' + name)
    return 'https://claduva.github.io/pdl_images/sprites/default.png'


def calculate_moveset(poke_identifier, poke_data, pokedex, moves, learnsets):
    moveset = {'gen' + str(i): [] for i in range(1, 9)}

    # Some mons like megas don't get a learnset, so we need to use their base specie's learnset
    reference_learnset_mon = poke_identifier
    if (poke_identifier not in learnsets) or ('learnset' not in learnsets[poke_identifier]):
        reference_learnset_mon = None
        base_species_identifier = [p for p in pokedex if 'baseSpecies' in poke_data and pokedex[p]['name'] == poke_data['baseSpecies']]
        if len(base_species_identifier) > 0:
            reference_learnset_mon = base_species_identifier[0]
    
    if (reference_learnset_mon is None) or (reference_learnset_mon not in learnsets) or ('learnset' not in learnsets[reference_learnset_mon]):
        print(f'{poke_identifier}\'s learnset not found')
        return {}
    
    for i in range(1, 9):
        for move_identifier, gens in learnsets[reference_learnset_mon]['learnset'].items():
            learn = [a for a in gens if a.startswith(str(i))]
            if len(learn) > 0:
                moveset['gen' + str(i)].append(moves[move_identifier]['name'])
    
    return moveset


def is_valid_pokemon(name, data):
    if data['num'] <= 0:  # Removing fakemons
        return False

    if 'forme' in data and data['forme'] in ['Alola-Totem']:
        return False

    if 'forme' in data and data['forme'] in ['Hisui', 'Galar', 'Alola', 'Gmax']:
        return True

    # Removing all variants irrelevant for drafting
    alternate_forms = ['Pikachu', 'Arceus', 'Pichu', 'Oricorio', 'Silvally', 'Genesect', 'Castform',
        'Wormadam', 'Aegislash', 'Eiscue', 'Morpeko', 'Pumpkaboo', 'Minior', 'Eternatus', 'Zarude', 
        'Indeedee', 'Polteageist', 'Sinistea', 'Cramorant', 'Magearna', 'Mimikyu', 'Xerneas', 
        'Wishiwashi', 'Gourgeist', 'Meowstic', 'Vivillon', 'Meloetta', 'Keldeo', 'Darmanitan', 
        'Darmanitan-Galar', 'Basculin', 'Cherrim']

    if 'baseSpecies' in data:
        if data['baseSpecies'] in alternate_forms:
            return False
    
    if data['name'] == 'Eevee-Starter' or data['name'].startswith('Toxtricity-Low'):
        return False
    
    return True


def calculate_type_effectiveness(poke_types, typechart):
    alltypes = ['Bug', 'Dark', 'Dragon', 'Electric', 'Fairy', 'Fighting', 'Fire', 'Flying', 
        'Ghost', 'Grass', 'Ground', 'Ice', 'Normal', 'Poison', 'Psychic', 'Rock', 'Steel', 'Water']
    
    type_effectiveness = {t: 0 for t in alltypes}

    for poke_type in poke_types:
        for attacker, value in typechart[poke_type.lower()]['damageTaken'].items():
            if attacker in alltypes:
                if type_effectiveness[attacker] == 3:
                    continue
                if value == 1: # Super Effective
                    type_effectiveness[attacker] += -1
                if value == 2: # Not Very Effective
                    type_effectiveness[attacker] += 1
                if value == 3: # Immune
                    type_effectiveness[attacker] = 3

    return type_effectiveness