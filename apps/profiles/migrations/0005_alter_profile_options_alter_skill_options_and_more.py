# Generated by Django 5.1 on 2024-09-06 13:53

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0004_alter_profile_options_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='profile',
            options={'ordering': ['-created']},
        ),
        migrations.AlterModelOptions(
            name='skill',
            options={'ordering': ['-created']},
        ),
        migrations.RemoveIndex(
            model_name='profile',
            name='profiles_pr_created_39264b_idx',
        ),
        migrations.AlterField(
            model_name='profile',
            name='bio',
            field=models.TextField(blank=True, verbose_name='Bio'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='location',
            field=models.CharField(blank=True, max_length=100, verbose_name='Location'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='photos/%Y/%m/%d/', verbose_name='Photo'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='short_intro',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Short Intro'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='social_github',
            field=models.URLField(blank=True, verbose_name='Social Github'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='social_linkedin',
            field=models.URLField(blank=True, verbose_name='Social LinkedIn'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='social_stackoverflow',
            field=models.URLField(blank=True, verbose_name='Social Stackoverflow'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='social_twitter',
            field=models.URLField(blank=True, verbose_name='Social Twitter'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='social_website',
            field=models.URLField(blank=True, verbose_name='Social Website'),
        ),
        migrations.AlterField(
            model_name='skill',
            name='description',
            field=models.TextField(blank=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='skill',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Name'),
        ),
        migrations.AddIndex(
            model_name='profile',
            index=models.Index(fields=['-created'], name='profiles_pr_created_a1bd98_idx'),
        ),
        migrations.AddIndex(
            model_name='profile',
            index=models.Index(fields=['short_intro'], name='profiles_pr_short_i_e9ca75_idx'),
        ),
    ]