from django import template
register = template.Library()

@register.filter(name='subtract')
def subtract(num, arg):
    try:
        return num-arg
    except:
        return 0