from django.db import models
from datetime import date
import pandas as pd

class Item(models.Model):
    title = models.TextField(blank = True)
    overview = models.TextField(blank = True)
    original_lan = models.TextField(blank = True)
    spoken_lan = models.TextField(blank = True)
    genres = models.TextField(blank = True)
    release_date = models.DateField(default = date(1111, 11, 11), blank = True, null = True)

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
            )
            for _, row in movie_dataset.iterrows()
        ], ignore_conflicts=True)
        print(">Done")




