# Item Recommendation and Retrieval System
> The following project implemented a custom search engine and a recommender systems using three dif- ferent methodologies, personalized search recommen- dations, content-based recommendations and collaborative filtering recommendations.

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
## in another terminal
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

* [**Nassim Habbash**](https://github.com/dodicin) (808292)
* [**Ricardo Matamoros**](https://github.com/ricardoanibalmatamorosaragon) (807450)
* [**Giacomo Villa**](https://github.com/Villone96) (807462)
