from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import date
import pandas as pd

class Profile(models.Model):
    #user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.TextField(blank = True)

    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(blank=True)

    # Profiling info
    genre_preferences = models.TextField(blank = True)
    history_profile = models.TextField(blank = True)
    language = models.TextField(blank = True)

    def __str__(self):
        return self.username

    ''''
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()
        def __str__(self):
            return self.name
    '''

    @classmethod
    def populate(cls):
        try:
            print("Trying clearing DB")
            cls.objects.all().delete()
            print(">Done")
        except Exception as e:
            print("Error:", e)
            print("Couldn't clear DB")

        users_dataset = pd.read_csv('./data/users.csv', delimiter = ";", keep_default_na=False)

        print("Populating")
        cls.objects.bulk_create([
            cls(
                username=row['username'],
                location=row['location'],
                birth_date=row['birth_date'],
                genre_preferences=row['genre_preferences'],
                history_profile=row['history_profile'],
                language=row['language']
            )
            for _, row in users_dataset.iterrows()
        ], ignore_conflicts=True)
        print(">Done")

    def get_genre_preferences(name):
        query = Profile.objects.get(username=name)
        return getattr(query, 'genre_preferences')
    
    def get_language(name):
        query = Profile.objects.get(username=name)
        return getattr(query, 'language')

class Item(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.TextField(blank = True)
    overview = models.TextField(blank = True)
    original_lan = models.TextField(blank = True)
    spoken_lan = models.TextField(blank = True)
    genres = models.TextField(blank = True)
    release_date = models.DateField(default = date(1111, 11, 11), blank = True, null = True)
    production_companies = models.TextField(blank = True)
    vote_average = models.IntegerField(blank = True)
    vote_count = models.IntegerField(blank = True)

    def __str__(self):
        return self.title

    @classmethod
    def populate(cls):
        try:
            print("Trying clearing DB")
            cls.objects.all().delete()
            print(">Done")
        except Exception as e:
            print("Error:", e)
            print("Couldn't clear DB")

        movie_dataset = pd.read_csv('./data/parsed_dataset.csv', delimiter = ";", keep_default_na=False)
        
        print("Populating")
        cls.objects.bulk_create([
            cls(
                id = row['id'],
                title=row['title'],
                overview=row['overview'],
                original_lan=row['original_language'],
                spoken_lan=row['spoken_languages'],
                genres=row['genres'],
                release_date=row['release_date'],
                production_companies=row['production_companies'],
                vote_average=row['vote_average'],
                vote_count=row['vote_count']
            )
            for _, row in movie_dataset.iterrows()
        ], ignore_conflicts=True)
        print(">Done")




