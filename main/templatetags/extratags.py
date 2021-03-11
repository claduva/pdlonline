from django import template
register = template.Library()

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
