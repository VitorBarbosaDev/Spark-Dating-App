from django import template
from profiles.models import Interest

register = template.Library()

@register.filter(name='icon_mapper')
def icon_mapper(interest):
    # Ensure interest is an Interest object and has a name attribute
    if not isinstance(interest, Interest) or not hasattr(interest, 'name'):
        return 'fas fa-star'  # Default icon

    # Convert interest name to lowercase
    interest_name_lower = interest.name.lower()

    # Debugging: print the interest_name being received
    print(f"Received interest name: {interest_name_lower}")

    mapping = {
        'music': 'fas fa-music',
        'sports': 'fas fa-football-ball',
        'travel': 'fas fa-plane',
        'food': 'fas fa-utensils',
        'fashion': 'fas fa-tshirt',
        'technology': 'fas fa-microchip',
        'politics': 'fas fa-landmark',
        'movies': 'fas fa-film',
        'books': 'fas fa-book',
        'health': 'fas fa-heartbeat',
        'art': 'fas fa-palette',
        'photography': 'fas fa-camera',
        'business': 'fas fa-briefcase',
        'education': 'fas fa-graduation-cap',
        'science': 'fas fa-atom',
        'gaming': 'fas fa-gamepad',
        'cooking': 'fas fa-blender',
    }

    # Return the corresponding icon class or default to 'fas fa-star'
    return mapping.get(interest_name_lower, 'fas fa-star')
