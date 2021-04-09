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

@register.filter(name='order_by')
def order_by(queryset, args):
    args = [x.strip() for x in args.split(',')]
    return queryset.order_by(*args)

@register.filter(name='reorder_group')
def reorder_group(groups):
    print(groups)
    return groups

@register.filter(name='sum_points')
def sum_points(qs):
    points=0
    for item in qs: 
        if item['points']: 
            points+=item['points']
    return points

@register.filter(name="subtract")
def subtract(value, arg):
    return value - arg

@register.filter(name="classfromdata")
def classfromdata(data):
    classstring=""
    for t in data['types']:
        classstring=classstring+f"type-{t.replace(' ','').replace('%','').replace(':','').replace('.','').lower()} "
    for a in data['abilities']:
        classstring=classstring+f"ability-{a.replace(' ','').replace('%','').replace(':','').replace('.','').lower()} "
    for m in data['movesets']['gen8']:
        classstring=classstring+f"move-{m.replace(' ','').replace('%','').replace(':','').replace('.','').lower()} "
    return classstring

@register.filter(name="converttoclass")
def converttoclass(string):
    string=string.replace(" ","").lower()
    return string