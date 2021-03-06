# Generated by Django 2.2 on 2020-01-08 11:28

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('title', models.TextField(blank=True, null=True)),
                ('overview', models.TextField(blank=True, null=True)),
                ('original_lan', models.TextField(blank=True, null=True)),
                ('spoken_lan', models.TextField(blank=True, null=True)),
                ('genres', models.TextField(blank=True, null=True)),
                ('release_date', models.DateField(blank=True, default=datetime.date(1111, 11, 11), null=True)),
                ('production_companies', models.TextField(blank=True, null=True)),
                ('vote_average', models.FloatField(blank=True, null=True)),
                ('vote_count', models.IntegerField(blank=True, null=True)),
                ('weighted_vote', models.FloatField(blank=True, null=True)),
                ('poster_path', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField(blank=True)),
                ('username', models.TextField(blank=True)),
                ('location', models.CharField(blank=True, max_length=30)),
                ('birth_date', models.DateField(blank=True)),
                ('genre_preferences', models.TextField(blank=True)),
                ('film_ratings', models.TextField(blank=True)),
                ('language', models.TextField(blank=True)),
            ],
        ),
    ]
