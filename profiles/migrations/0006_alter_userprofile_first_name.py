# Generated by Django 4.2.9 on 2024-01-12 22:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0005_alter_feedback_options_alter_interest_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='first_name',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
