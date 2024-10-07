# Generated by Django 5.1.1 on 2024-09-22 18:34

import autoslug.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0008_alter_review_project'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='slug',
            field=autoslug.fields.AutoSlugField(always_update=True, default='slug', editable=False, populate_from=models.CharField(max_length=255, verbose_name='Title')),
            preserve_default=False,
        ),
    ]