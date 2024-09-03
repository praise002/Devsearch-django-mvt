# Generated by Django 5.1 on 2024-09-03 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_remove_user_photo'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='user',
            index=models.Index(fields=['username'], name='accounts_us_usernam_c0ea66_idx'),
        ),
    ]
