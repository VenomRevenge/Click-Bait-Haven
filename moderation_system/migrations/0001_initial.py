# Generated by Django 5.1.2 on 2024-11-27 21:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('profiles', '0003_alter_profile_profile_picture'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_of_review', models.DateTimeField(auto_now_add=True)),
                ('viewed', models.BooleanField(default=False)),
                ('is_positive_review', models.BooleanField(default=True)),
                ('reason_for_rejection', models.TextField(help_text='Enter a reason for why the article is rejected.', max_length=500)),
                ('article_title', models.CharField(max_length=50)),
                ('article_id', models.PositiveIntegerField(blank=True, null=True)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to='profiles.profile')),
                ('reviewer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='notification_reviews', to='profiles.profile')),
            ],
        ),
    ]
