# Generated by Django 5.1 on 2024-09-03 13:54

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_profile_photo'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='profile',
            options={},
        ),
        migrations.RemoveIndex(
            model_name='profile',
            name='profiles_pr_created_39264b_idx',
        ),
        migrations.AddIndex(
            model_name='profile',
            index=models.Index(fields=['short_intro'], name='profiles_pr_short_i_e9ca75_idx'),
        ),
    ]