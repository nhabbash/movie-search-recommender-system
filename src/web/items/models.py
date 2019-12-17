from django.db import models
from datetime import date
import pandas as pd

class Consumer(models.Model):
    name = models.TextField(blank = True)
    interest = models.TextField(blank = True)

    def __str__(self):
        return self.name

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
                name=row['name'],
                interest=row['interest']
            )
            for _, row in users_dataset.iterrows()
        ], ignore_conflicts=True)
        print(">Done")

    def get_interest(name):
        query = Consumer.objects.get(name=name)
        return getattr(query, 'interest')

class Item(models.Model):
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




