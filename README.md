# Item Recommendation and Retrieval System
>TODO

## Brief

TODO

## Prerequisites

* Python 3.7 or higher
* Docker
* Docker Compose

## Installation
```sh
$ git clone https://github.com/dodicin/item-recommendation-retrieval-system
$ cd item-recommendation-retrieval-system/src
```
## Structure



## Starting the containers
```sh
$ sudo docker-compose build 
$ sudo docker-compose up
```

## Utilities
```sh
$ sudo docker-compose run web python3 manage.py startapp {app_name} # Creates {app_name} in the project (after building)
$ sudo docker exec -it web bash # Entering the web container
$ python manage.py createsuperuser # Creating super user 
$ python manage.py makemigrations 
$ python manage.py migrate
```


## Authors

* [**Nassim Habbash**](https://github.com/dodicin) (808292)
* [**Ricardo Matamoros**](https://github.com/ricardoanibalmatamorosaragon) (807450)
* [**Giacomo Villa**](https://github.com/Villone96) (807462)
