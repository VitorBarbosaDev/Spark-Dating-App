"""
Enable Row Level Security (RLS) on all public tables.

Supabase exposes the public schema via PostgREST. Without RLS, any client
with the anon or authenticated key can read/write every table. Enabling RLS
with no permissive policies blocks PostgREST access while Django (which
connects as the table owner) is unaffected — PostgreSQL skips RLS checks
for the table owner by default.
"""

from django.db import migrations

# Every table visible in the Supabase Table Editor / Security Advisor.
TABLES = [
    # --- about app ---
    "about_about",
    "about_teammember",
    # --- allauth / account ---
    "account_emailaddress",
    "account_emailconfirmation",
    # --- auth ---
    "auth_group",
    "auth_group_permissions",
    "auth_permission",
    "auth_user",
    "auth_user_groups",
    "auth_user_user_permissions",
    # --- django internals ---
    "django_admin_log",
    "django_content_type",
    "django_migrations",
    "django_session",
    "django_site",
    "django_summernote_attachment",
    # --- messaging app ---
    "messaging_message",
    # --- profiles app ---
    "profiles_feedback",
    "profiles_interest",
    "profiles_match",
    "profiles_message",
    "profiles_report",
    "profiles_swipe",
    "profiles_userprofile",
    "profiles_userprofile_blocked_users",
    "profiles_userprofile_groups",
    "profiles_userprofile_interests",
    "profiles_userprofile_user_permissions",
    "profiles_userprofileimage",
    # --- socialaccount ---
    "socialaccount_socialaccount",
    "socialaccount_socialapp",
    "socialaccount_socialapp_sites",
    "socialaccount_socialtoken",
]


def enable_rls(apps, schema_editor):
    """Enable RLS on all tables (PostgreSQL only, skipped on SQLite)."""
    if schema_editor.connection.vendor != "postgresql":
        return
    for table in TABLES:
        schema_editor.execute(
            f"ALTER TABLE IF EXISTS public.{table} ENABLE ROW LEVEL SECURITY;"
        )


def disable_rls(apps, schema_editor):
    """Reverse: disable RLS on all tables."""
    if schema_editor.connection.vendor != "postgresql":
        return
    for table in TABLES:
        schema_editor.execute(
            f"ALTER TABLE IF EXISTS public.{table} DISABLE ROW LEVEL SECURITY;"
        )


class Migration(migrations.Migration):

    dependencies = [
        ("profiles", "0006_alter_userprofile_first_name"),
    ]

    operations = [
        migrations.RunPython(enable_rls, reverse_code=disable_rls),
    ]
