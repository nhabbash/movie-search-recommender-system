# Movie Search and Recommender System
> Movie search engine and recommender system with ElasticSearch, Django and scikit-learn

## Overview
The following project implemented a custom search engine and a recommender systems for retrieving movies and recommending new ones based on a personal scoring list.
The recommendations are made through three different methodologies, personalized search, content-based similarity and collaborative filtering.

#### [Documentatation](docs/report.pdf)
#### [Presentation](docs/presentation.pdf)

## Prerequisites
* Python 3.7 or higher
* Docker
* Docker Compose

## Installation
```sh
$ git clone https://github.com/dodicin/item-recommendation-retrieval-system
$ cd item-recommendation-retrieval-system/src
```

## First time setup
```sh
$ sudo docker-compose build 
$ sudo docker-compose up
$ sudo docker exec -it item-retrieval-web bash # Entering the web container
$ python manage.py makemigrations 
$ python manage.py migrate
$ python init_data.py (items/profiles/"") # Initialize data (creates superuser, clears and populates DB, refreshes index)
```

## Starting app 
```sh
$ sudo docker-compose up 
```

## Resources 
* Search Engine: `localhost:8000/items`
* Recommender System: `localhost:8000/items/recommender`

## Notes
Users are in `src\web\data\users.csv`

## Authors

* [**Nassim Habbash**](https://github.com/nhabbash) (808292)
* [**Ricardo Matamoros**](https://github.com/ricardoanibalmatamorosaragon) (807450)
* [**Giacomo Villa**](https://github.com/Villone96) (807462)
