from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import date
import pandas as pd

from django.db import connection

class Profile(models.Model):
    #user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_id = models.IntegerField(blank = True) 
    username = models.TextField(blank = True)

    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(blank=True)

    # Profiling info
    genre_preferences = models.TextField(blank = True)
    film_ratings = models.TextField(blank = True)
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

            cursor = connection.cursor()
            cursor.execute("TRUNCATE " + str(cls.objects.model._meta.db_table))
            #cls.objects.all()._raw_delete(cls.db)
            print(">Done")
        except Exception as e:
            print("Error:", e)
            print("Couldn't clear DB")

        users_dataset = pd.read_csv('./data/users.csv', delimiter = ",", keep_default_na=False)

        print("Populating")
        cls.objects.bulk_create([
            cls(
                user_id=row['user_id'],
                username=row['username'],
                location=row['location'],
                birth_date=row['birth_date'],
                genre_preferences=row['genre_preferences'],
                film_ratings=row['film_ratings'],
                language=row['language']
            )
            for _, row in users_dataset.iterrows()
        ], ignore_conflicts=True)
        print(">Done")

    def get_genre_preferences(name):
        try:
            query = Profile.objects.get(username=name)
            return getattr(query, 'genre_preferences')
        except:
            return ""
    
    def get_language(name):
        try:
            query = Profile.objects.get(username=name)
            return getattr(query, 'language')
        except:
            return ""

    def get_id(name):
        try:
            query = Profile.objects.get(username=name)
            return getattr(query, 'user_id')
        except:
            return ""
    
    def get_films(name):
        try:
            query = Profile.objects.get(username=name)
            return getattr(query, 'film_ratings')
        except:
            return ""



class Item(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.TextField(blank = True, null = True)
    overview = models.TextField(blank = True, null = True)
    original_lan = models.TextField(blank = True, null = True)
    spoken_lan = models.TextField(blank = True, null = True)
    genres = models.TextField(blank = True, null = True)
    release_date = models.DateField(default = date(1111, 11, 11), blank = True, null = True)
    production_companies = models.TextField(blank = True, null = True)
    vote_average = models.FloatField(blank = True, null = True)
    vote_count = models.IntegerField(blank = True, null = True)
    weighted_vote = models.FloatField(blank = True, null = True)

    poster_path = models.TextField(blank = True, null = True)

    def __str__(self):
        return self.title

    @classmethod
    def populate(cls):
        try:
            print("Trying clearing DB")
            cursor = connection.cursor()
            cursor.execute("TRUNCATE " + str(cls.objects.model._meta.db_table))
            #cls.objects.all()._raw_delete(cls.db)
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
                vote_count=row['vote_count'],
                weighted_vote=row['weighted_vote'],
                poster_path=row['poster_path'],
            )
            for _, row in movie_dataset.iterrows()
        ], ignore_conflicts=True)
        print(">Done")

    def get_item(id):
        try:
            obj = Item.objects.get(pk = id)
            return obj
        except:
            return ""




