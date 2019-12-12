import pandas as pd
import csv
import os
import json

def get_element(values, word):
    contents = ""
    index = 0
    if values == values:
        text = values.split("'")
        for element in text:
            if word in element:
                contents += text[index + 2] + " "
            index += 1
    return contents

fields = ['genres', 'id', 'original_language', 'overview', 'spoken_languages', 'title', 'release_date']
movie_dataset = pd.read_csv('src/web/data/dataset.csv', usecols=fields)

if not os.path.exists('src/web/data/parsed_dataset.csv'):
    with open('src/web/data/parsed_dataset.csv', 'w', newline='') as file:
        writer = csv.writer(file, delimiter =";")
        writer.writerow(["id", "title", "overview", 'original_language', 'spoken_languages', 'genres', 'release_date'])
        for index, row in movie_dataset.iterrows():

            spoken = get_element(row['spoken_languages'], 'iso')
            genres = get_element(row['genres'], 'name')

            if 'nan' in str(row['release_date']):
                date = ""
            else:
                date = row['release_date']

            if not(row['title'] == "" or row['overview'] == ""):
                writer.writerow([row['id'], row['title'], row['overview'], row['original_language'], spoken, genres, date])