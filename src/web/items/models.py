from django.db import models
import pandas as pd

class Item(models.Model):
    title = models.TextField(blank = True, null = True)
    overview = models.TextField(blank = True, null = True)
    original_lan = models.TextField(blank = True, null = True)
    spoken_lan = models.TextField(blank = True, null = True)
    genres = models.TextField(blank = True, null = True)
    data = models.DateField(default = None, blank = True, null = True)

    def __str__(self):
        return self.title

    @classmethod
    def populate(delfault_value = 1):
        import datetime

        movie_dataset = pd.read_csv('./data/parsed_dataset.csv', delimiter = ";")
        for index, row in movie_dataset.iterrows():
            # data = datetime.datetime.strptime(row['date'], '%Y-%m-%d')
            
            try: 
                film = Item(title = row['title'], overview = row['overview'], original_lan = row['original_language'],
                spoken_lan = row['spoken_languages'], genres = row['genres'], data = row['release_date'])
                film.save()  
            except Exception as e: 
                print("ERROR SOURCE:", row['title'])
                print(e)
                print("")



