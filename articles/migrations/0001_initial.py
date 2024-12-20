# Generated by Django 5.1.2 on 2024-11-10 22:49

import django.core.validators
import django.db.models.deletion
import profiles.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('profiles', '0003_alter_profile_profile_picture'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True, validators=[django.core.validators.MinLengthValidator(limit_value=3)])),
            ],
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, unique=True, validators=[django.core.validators.MinLengthValidator(limit_value=10)])),
                ('content', models.TextField(max_length=15000, validators=[django.core.validators.MinLengthValidator(limit_value=500)])),
                ('picture', models.ImageField(blank=True, help_text='The article picture will be automatically resized to 1920x1080px', null=True, upload_to='article_pictures', validators=[profiles.validators.validate_image_size])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_approved', models.BooleanField(default=False)),
                ('approved_at', models.DateTimeField(blank=True, null=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('approved_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='approved_articles', to='profiles.profile')),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='articles', to='profiles.profile')),
                ('tags', models.ManyToManyField(to='articles.tag')),
            ],
        ),
    ]
