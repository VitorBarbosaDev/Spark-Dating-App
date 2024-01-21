from ..utils import icon_mapper
from django import template

register = template.Library()

@register.filter(name='icon_mapper')
def icon_mapper_filter(interest):
    return icon_mapper(interest)