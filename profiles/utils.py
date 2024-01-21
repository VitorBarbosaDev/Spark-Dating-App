from .models import Interest


def gender_icon_mapper(gender):
    icons = {
        'Male': 'fas fa-mars',
        'Female': 'fas fa-venus',
        'Other': 'fas fa-genderless',
        'Prefer not to say': 'fas fa-question',
    }
    return icons.get(gender, 'fas fa-question')


def icon_mapper(interest):
        # Ensure interest is an Interest object and has a name attribute
        if not isinstance(interest, Interest) or not hasattr(interest, 'name'):
            return 'fas fa-star'  # Default icon

        # Convert interest name to lowercase
        interest_name_lower = interest.name.lower()


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
