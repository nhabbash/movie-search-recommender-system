import pandas as pd
import csv
import os
import json
from datetime import datetime

def get_element(values, word):
    contents = ""
    index = 0
    if values == values:
        text = values.split("'")
        for element in text:
            if word in element:
                contents += text[index + 2] + ", "
            index += 1
    return contents

fields = ['id', 'genres', 'original_language', 'overview', 'spoken_languages', 'title', 'release_date', 
            'production_companies', 'vote_average','vote_count']
movie_dataset = pd.read_csv('src/web/data/dataset.csv', usecols=fields, keep_default_na=False)

if not os.path.exists('src/web/data/parsed_dataset.csv'):
    with open('src/web/data/parsed_dataset.csv', 'w', newline='') as file:
        writer = csv.writer(file, delimiter =";")
        writer.writerow(["id", "title", "overview", 'original_language', 'spoken_languages', 'genres', 
                'release_date', 'production_companies', 'vote_average', 'vote_count'])
        for index, row in movie_dataset.iterrows():
            spoken = get_element(row['spoken_languages'], 'iso')
            genres = get_element(row['genres'], 'name')
            companies = get_element(row['production_companies'], 'name')
            date = row['release_date']
  
            try:
                date = datetime.strptime(date, '%Y-%m-%d').date()
            except:
                date = "1900-01-01"

            if not row['id']:
                row['id'] = max(movie_dataset.id) + 1
                print(row['id'])

            if row['title'] and row['overview']:
                writer.writerow([row['id'], row['title'], row['overview'], row['original_language'], spoken, 
                        genres, date, companies, row['vote_average'], row['vote_count']])