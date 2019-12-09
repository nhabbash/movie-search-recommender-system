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

fields = ['genres', 'id', 'original_language', 'overview', 'spoken_languages', 'title']
movie_dataset = pd.read_csv('./data/dataset.csv', usecols=fields)

if not os.path.exists('./data/parsed_dataset.csv'):
    with open('./data/parsed_dataset.csv', 'w', newline='') as file:
        writer = csv.writer(file, delimiter =";")
        writer.writerow(["Id", "Title", "Overview", 'Original_Language', 'Spoken_Languages', 'Genres'])
        for index, row in movie_dataset.iterrows():

            spoken = get_element(row['spoken_languages'], 'iso')
            genres = get_element(row['genres'], 'name')

            if not(row['title'] == "" or row['overview'] == ""):
                writer.writerow([row['id'], row['title'], row['overview'], row['original_language'], spoken, genres])