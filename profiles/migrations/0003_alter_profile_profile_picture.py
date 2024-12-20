# Generated by Django 5.1.2 on 2024-11-09 19:58

import profiles.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_profile_date_of_birth'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_picture',
            field=models.ImageField(blank=True, help_text='Your profile picture will be automatically resized to 500x500px', null=True, upload_to='profile_pictures', validators=[profiles.validators.validate_image_size]),
        ),
    ]
