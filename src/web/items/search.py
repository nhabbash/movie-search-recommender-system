from django.shortcuts import render
from items.documents import ItemDocument
from elasticsearch_dsl.query import Q
from .models import Profile, Item
import pandas as pd
import ast

def query(query_text, profile, personalized, fuzzy, synonyms, pop, weight):

    should_queryset = []
    must_queryset = []

    interest = ""
    language = ""
    fuzzyness_value = ""
    synonyms_value = ""
    prefix_value = 0
    leaf_query_type = "multi_match"
    items = []

    if fuzzy:
        fuzzyness_value = "AUTO"
        prefix_value = 2
    else:
        fuzzyness_value = "0"

    if synonyms:
        synonyms_value = "true"
    else:
        synonyms_value = "false"

    if personalized :
        interest = Profile.get_genre_preferences(profile)
        language = Profile.get_language(profile)

        if interest and language:
            should_queryset.extend([
                Q({"multi_match":                                       # Query type
                        {"query": interest,                             # User genre preference
                        "fields": ['genres^4', 'overview'],             # Boosting results in the genre field compared to the overview field
                        "type": "best_fields",
                        }
                    }),
                    Q({"multi_match":                                   # Query type
                        {"query": language,                             # User language preference
                        "fields": ['spoken_lan^10', 'original_lan'],
                        "type": "best_fields",
                        }
                    }),
            ])

    if query_text :
        if query_text[0] == query_text[-1] == "\"" :
            leaf_query_type = "match_phrase"

        if leaf_query_type == "multi_match":
            must_queryset.extend([
                Q({leaf_query_type:                                       # Query type
                        {"query": query_text, 
                        "fields": ['title^4', 'overview^3', 'production_companies'],              # Boosting results in the title field compared to the overview field
                        "fuzziness": fuzzyness_value,                            # Lets search for words with typos in them
                        "prefix_length": prefix_value,
                        "auto_generate_synonyms_phrase_query": synonyms_value,  # Generates words synonims if possible in the query (ny = new and york)
                        "type": "best_fields",
                        }
                    }),
            ])
        elif leaf_query_type == "match_phrase" :
            must_queryset.extend([
                Q({leaf_query_type:                                       # Query type
                        {"title": query_text}
                    }),
            ])
    
    if weight :
    # Relevance dimension using Rank Feature datatype in the index
         query = Q(
            {"function_score" : {
                "query": Q(
                    "bool",
                    must = must_queryset,         # Main query
                    should = should_queryset,     # Personalization
                    minimum_should_match = "20%",
                    ),
                "field_value_factor": {
                    "field": "weighted_vote",
                    "factor": 1.2,
                    "modifier": "sqrt",
                    "missing": 1
                    }
                }
            }
        )
    
    elif pop :
    # Relevance dimension using Function Score query
        query = Q(
            {"function_score" : {
                "query": Q(
                    "bool",
                    must = must_queryset,         # Main query
                    should = should_queryset,     # Personalization
                    minimum_should_match = "20%",
                    ),
                "field_value_factor": {
                    "field": "vote_count",
                    "factor": 1.2,
                    "modifier": "sqrt",
                    "missing": 1
                    }
                }
            }
        )
    else :
        query = Q(
            "bool",
            must = must_queryset,         # Main query
            should = should_queryset,     # Personalization
            minimum_should_match = "20%",
            )

    if query_text or profile:
        items = ItemDocument.search().query(query)

    return items, interest, language

def clean_film_rating(dirty_films_rating): 
    # films_with_rating = dirty_films_rating.replace("[", "").replace("]", "").replace(" ", "").replace("(", "").replace(")", "").split(",")
    films_with_rating = ast.literal_eval(dirty_films_rating)
    films = list()
    index = 0
    films = films_with_rating
    return films

def recommendation(profile, filtering):

    film_cf = list()
    film_cb = list()
    profile_seen = list()
    interest = ""
    language = ""

    if profile:
        user_id = Profile.get_id(profile)
        interest = Profile.get_genre_preferences(profile)
        language = Profile.get_language(profile)

        if not filtering:
            recommandations_dataset = pd.read_csv('./data/user_recommender.csv', keep_default_na=False)
        else:
            recommandations_dataset = pd.read_csv('./data/user_recommender_filter.csv', keep_default_na=False)

        
        for _, row in recommandations_dataset.iterrows():
            if row['userId'] == user_id:
                if row['type_r'] == 'cf':
                    x = {}
                    x["film"] = Item.get_item(int(row['movieId']))
                    x["score"] = row['rank']
                    film_cf.append(x)
                elif row['type_r'] == 'cb':
                    x = {}
                    x["film"] = Item.get_item(int(row['movieId']))
                    x["score"] = row['rank']
                    film_cb.append(x)

        films = Profile.get_films(profile)
        user_ratings = ast.literal_eval(films)

        for couple in user_ratings:
            x = {}
            x["film"] = Item.get_item(couple[0])
            x["score"] = couple[1]
            profile_seen.append(x)

    return film_cf, film_cb, profile_seen, interest, language
    