from django.db import models
import pandas as pd

class Item(models.Model):
    title = models.TextField(blank = True)
    overview = models.TextField(blank = True)
    original_lan = models.TextField(blank = True)
    spoken_lan = models.TextField(blank = True)
    genres = models.TextField(blank = True)
    date = models.DateField(default=None, blank = True, null = True)

    def __str__(self):
        return self.title

    @classmethod
    def populate(delfault_value = 1):

        movie_dataset = pd.read_csv('./data/parsed_dataset.csv', delimiter = ";", keep_default_na=False)
        for _, row in movie_dataset.iterrows():
            
            try: 
                if row['release_date'] == "":
                   row['release_date'] = None 
                   
                film = Item(title = row['title'], overview = row['overview'], original_lan = row['original_language'],
                spoken_lan = row['spoken_languages'], genres = row['genres'], date = row['release_date'])
                film.save()  
            except Exception as e: 
                print("ERROR SOURCE: ")
                print(row)
                print("Error:", e)
                print("")



