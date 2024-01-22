from django import template

register = template.Library()

@register.filter(name='range_filter')
def range_filter(start, end):
    return range(start, end)
