# Generated by Django 4.2.9 on 2024-01-11 21:42

import cloudinary.models
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('age', models.PositiveIntegerField(blank=True, null=True)),
                ('gender', models.CharField(blank=True, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other'), ('Prefer not to say', 'Prefer not to say')], max_length=50)),
                ('interests', models.CharField(blank=True, choices=[('Sports', 'Sports'), ('Music', 'Music'), ('Movies', 'Movies'), ('Books', 'Books'), ('Art', 'Art')], max_length=200)),
                ('bio', models.TextField(blank=True)),
                ('interested_in', models.CharField(blank=True, choices=[('Men', 'Men'), ('Women', 'Women'), ('Both', 'Both'), ('None', 'None')], max_length=50)),
                ('feedback_count', models.PositiveIntegerField(default=0)),
                ('unread_messages_count', models.PositiveIntegerField(default=0)),
                ('swipes_count', models.PositiveIntegerField(default=0)),
                ('account_status', models.CharField(default='active', max_length=50)),
                ('location', models.CharField(blank=True, max_length=100)),
                ('last_swipe', models.DateTimeField(blank=True, null=True)),
                ('feedback_submitted', models.TextField(blank=True)),
                ('show_age', models.BooleanField(default=True)),
                ('show_distance', models.BooleanField(default=True)),
                ('profile_visibility', models.BooleanField(default=True)),
                ('show_me_in_discovery', models.BooleanField(default=True)),
                ('search_distance', models.PositiveIntegerField(default=10)),
                ('search_age_range_min', models.PositiveIntegerField(default=18)),
                ('search_age_range_max', models.PositiveIntegerField(default=100)),
                ('message_notifications', models.BooleanField(default=True)),
                ('reports_made', models.IntegerField(default=0)),
                ('blocked_users', models.ManyToManyField(blank=True, to='profiles.userprofile')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='userprofile_set', related_query_name='userprofile', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='userprofile_set', related_query_name='userprofile', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='UserProfileImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', cloudinary.models.CloudinaryField(max_length=255, verbose_name='image')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='profiles.userprofile')),
            ],
        ),
        migrations.CreateModel(
            name='Swipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('liked', models.BooleanField(default=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('swiped_on', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='swipes_received', to='profiles.userprofile')),
                ('swiper', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='swipes_made', to='profiles.userprofile')),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('reported_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reports_received', to='profiles.userprofile')),
                ('reporting_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_reports_made', to='profiles.userprofile')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('read', models.BooleanField(default=False)),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages_received', to='profiles.userprofile')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages_sent', to='profiles.userprofile')),
            ],
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('user1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='matches_user1', to='profiles.userprofile')),
                ('user2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='matches_user2', to='profiles.userprofile')),
            ],
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('message', models.TextField()),
                ('read', models.BooleanField(default=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='feedbacks', to='profiles.userprofile')),
            ],
        ),
    ]
