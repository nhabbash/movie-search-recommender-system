import pandas as pd
import numpy as np
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
    
    return contents.rstrip(', ')

fields = ['id', 'genres', 'original_language', 'overview', 'spoken_languages', 'title', 'release_date', 
            'production_companies', 'vote_average','vote_count', 'poster_path']
movie_dataset = pd.read_csv('src/web/data/dataset.csv', usecols=fields, keep_default_na=False)

if not os.path.exists('src/web/data/parsed_dataset.csv'):
    with open('src/web/data/parsed_dataset.csv', 'w', newline='') as file:
        writer = csv.writer(file, delimiter =";")
        writer.writerow(["id", "title", "overview", 'original_language', 'spoken_languages', 'genres', 
                'release_date', 'production_companies', 'vote_average', 'vote_count', 'weighted_vote', 'poster_path'])
        for index, row in movie_dataset.iterrows():
            spoken = get_element(row['spoken_languages'], 'iso')
            genres = get_element(row['genres'], 'name')
            companies = get_element(row['production_companies'], 'name')
            date = row['release_date']
            poster_ur = "http://image.tmdb.org/t/p/w185/"+row['poster_path']
            
            
            weighted_vote = 0
            try:
                # TODO: use real mean global vote and count threshold
                # weighted rating (WR) = (v ÷ (v+m)) × R + (m ÷ (v+m)) × C 
                count_threshold = 3000
                avg_global_vote = 6.9
                vote = float(row['vote_average'])
                count = float(row['vote_count'])
                weighted_vote = (count/(count+count_threshold))*vote + (count_threshold/(count+count_threshold))*avg_global_vote
            except:
                pass
            
            try:
                date = datetime.strptime(date, '%Y-%m-%d').date()
            except:
                date = "1900-01-01"

            if not row['id']:
                row['id'] = max(movie_dataset.id) + 1
                print(row['id'])

            if row['title'] and row['overview']:
                writer.writerow([row['id'], row['title'], row['overview'], row['original_language'], spoken, 
                        genres, date, companies, row['vote_average'], row['vote_count'], weighted_vote, poster_ur])

parsed_data = pd.read_csv('src/web/data/parsed_dataset.csv', delimiter=";")

for _, row in parsed_data.iterrows():
    try:
        if "ro" in row['spoken_languages']: # or "zh" in row['spoken_languages']: # or "ru" in row['spoken_languages']:
                # if 'Fantasy' in row['genres'] or 'Adventure' in row['genres']:
                    print(row['id'])
                    print(row['title'])
                    print("")
    except:
            pass
# "Fantasy, Adventure, Crime, Romance","ja, zh"
#(32388, 4.0), (64847, 3.0), (400136, 2.0), (66105, 3.5), (83088, 1.5), (52103, 4.0), (32388, 5.0), (182030, 1.5), (163202, 3.5), (366170, 1.0), (44458, 3.0), (39962, 4.5), (406099, 1.5), (392882, 3.5), (83090, 3.5)"