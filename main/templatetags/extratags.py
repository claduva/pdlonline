from django import template
register = template.Library()

@register.filter(name='replace_spaces')
def replace_spaces(string):
    return string.replace(" ","_")

@register.filter(name='subtract')
def subtract(num, arg):
    try:
        return num-arg
    except:
        return 0
