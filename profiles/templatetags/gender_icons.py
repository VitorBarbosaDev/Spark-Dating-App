from ..utils import gender_icon_mapper
from django import template

register = template.Library()

@register.filter(name='gender_icon')
def gender_icon_filter(gender):
    return gender_icon_mapper(gender)
