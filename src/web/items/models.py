from django.db import models
import pandas as pd

class Item(models.Model):
    title = models.TextField()
    overview = models.TextField()
    original_lan = models.TextField()
    spoken_lan = models.TextField()
    genres = models.TextField()
    data = models.DateField(default = None, blank = True, null = True)

    def __str__(self):
        return self.title

    @classmethod
    def populate(delfault_value = 1):
        import datetime

        movie_dataset = pd.read_csv('./data/parsed_dataset.csv', delimiter = ";")
        for index, row in movie_dataset.iterrows():
            data = datetime.datetime.strptime(row['date'], '%Y-%m-%d')

            film = Item(title = row['title'], overview = row['overview'], original_lan = row['original_language'],
                        spoken_lan = row['spoken_languages'], genres = row['genres'], data = data)
            film.save()

