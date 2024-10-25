from django import template

register = template.Library()

@register.filter
def to_ands(value):
    return value.replace(" ","_")