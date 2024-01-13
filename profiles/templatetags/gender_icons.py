from django import template

register = template.Library()

@register.filter(name='gender_icon')
def gender_icon(gender):
    icons = {
        'Male': 'fas fa-mars',          # Font Awesome icon for male
        'Female': 'fas fa-venus',       # Font Awesome icon for female
        'Other': 'fas fa-genderless',   # Font Awesome icon for other/non-binary
        'Prefer not to say': 'fas fa-question', # Font Awesome icon for prefer not to say
    }
    return icons.get(gender, 'fas fa-question')  # Default icon
