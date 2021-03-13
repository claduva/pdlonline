from django import template
register = template.Library()
from accounts.models import CustomUser

@register.filter(name='pokedexnumber')
def pokedexnumber(int):
    if int<10:
        return "00"+str(int)
    elif int<100:
        return "0"+str(int)
    else:
        return str(int)

@register.filter(name='replace_spaces')
def replace_spaces(string):
    return string.replace(" ","_")

@register.filter(name='subtract')
def subtract(num, arg):
    try:
        return num-arg
    except:
        return 0

@register.filter(name='getpfp')
def getpfp(user):
    return f"https://cdn.discordapp.com/avatars/{user.discordid}/{user.avatar}"