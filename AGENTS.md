# AGENTS.md

## Project Overview

Spark Dating App — a Django 4.2 dating platform deployed on Heroku. Users sign up, build profiles with Cloudinary-hosted images, swipe on other users, match mutually, and chat. The project uses a **custom user model** (`profiles.UserProfile` extends `AbstractUser`), which is critical to understand before touching any auth or user-related code.

## Architecture

Three Django apps, all server-rendered with Bootstrap 5 templates:

- **`profiles/`** — Core app. Owns the custom user model (`UserProfile`), all dating models (`Swipe`, `Match`, `Message`, `Report`, `Feedback`), swiping logic, and the homepage. The home view (`/`) doubles as the discovery feed for authenticated users and a landing page for anonymous visitors.
- **`messaging/`** — Has its own `Message` model (separate from `profiles.Message`). Handles match list display and chat views. Uses the `messaging` URL namespace.
- **`about/`** — Simple CMS-style app for About page content managed via Django admin with Summernote.

### Key Data Flow: Swiping → Matching → Messaging

1. `home_view` filters `UserProfile` by gender preference, mutual interest, blocked users, and prior swipes, then paginates 1-at-a-time.
2. `like_user` / `dislike_user` create `Swipe` records. On mutual like, a `Match` is created.
3. `messaging.match_list` queries `Match` objects to show matched users.
4. `messaging.chat_view` and `get_new_messages` handle conversation via POST form submission and AJAX polling.

## Critical Conventions

- **Custom auth model**: `AUTH_USER_MODEL = 'profiles.UserProfile'`. Always use `UserProfile` (not `django.contrib.auth.User`) when creating test users or referencing the user model. See `profiles/test_views.py` for the pattern: `UserProfile.objects.create_user(username=..., password=..., gender=..., interested_in=...)`.
- **Environment config**: Secrets live in `env.py` (loaded via `import env` if file exists) and `.env` (loaded via `python-dotenv`). Required vars: `DATABASE_URL`, `SECRET_KEY`, `CLOUDINARY_URL`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`. Set `DEVELOPMENT=True` for `DEBUG=True`.
- **Images**: Profile images use `CloudinaryField` on `UserProfileImage`, not file-based storage. No `MEDIA_ROOT`/`MEDIA_URL` config exists.
- **Template tags**: Custom filters in `profiles/templatetags/` — `gender_icons.py`, `interest_icons.py`, `custom_filters.py`. Icon mapping logic lives in `profiles/utils.py` (`gender_icon_mapper`, `icon_mapper`).
- **Forms**: Signup uses allauth's `SignupForm` extended in `profiles/signup_forms.py` (`ACCOUNT_FORMS` in settings). Profile editing uses `ProfileForm` in `profiles/forms.py`.
- **Admin**: Rich text fields use `SummernoteModelAdmin`. `UserProfileAdmin` uses inline models for images and interests.
- **URL namespacing**: `messaging` app uses namespace — reference URLs as `messaging:match_list`, `messaging:chat`, `messaging:get_new_messages`. Profile URLs have no namespace.

## Development Commands

```bash
# Activate virtualenv
myenv\Scripts\activate        # Windows
source myenv/bin/activate     # Unix

# Install dependencies
pip install -r requirements.txt

# Run dev server (requires env.py or .env with DATABASE_URL)
python manage.py runserver

# Run all tests (uses SQLite automatically via settings.py)
python manage.py test

# Run tests for a specific app
python manage.py test profiles
python manage.py test messaging

# Migrations
python manage.py makemigrations
python manage.py migrate
```

## Testing Patterns

- Tests use Django's `TestCase`. SQLite is forced for tests via `if 'test' in sys.argv` in `settings.py`.
- Test files per app: `profiles/test_model.py`, `profiles/test_forms.py`, `profiles/test_views.py`, `messaging/test_models_messaging.py`, `messaging/test_views_messaging.py`.
- Always create users with `UserProfile.objects.create_user(...)` including `gender` and `interested_in` fields — the discovery feed filters on these.
- Swipe/match tests require two users with complementary gender preferences to trigger match creation logic.

## Frontend Stack

- Bootstrap 5 (CDN), Font Awesome 5 (CDN), jQuery 3.5.1 (CDN).
- Single CSS file: `static/css/style.css` with CSS custom properties (`--primary-color`, `--secondary-color`, etc.).
- Templates extend `templates/base.html`. App templates are in `<app>/templates/<app>/`.
- Swipe interactions use AJAX (`X-Requested-With: XMLHttpRequest` check in `home_view`) returning JSON with profile data.

## Deployment

- Heroku via `Procfile` (`web: gunicorn dating_app.wsgi`).
- Static files served by WhiteNoise. Run `python manage.py collectstatic` before deploy.
- Database: PostgreSQL via `dj-database-url` (Supabase-hosted). Cloudinary for image CDN.
- Runtime: `python-3.9.18` (see `runtime.txt`).

