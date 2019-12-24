from django.shortcuts import render
from items.documents import ItemDocument
from elasticsearch_dsl.query import Q
from .models import Profile

def query(query_text, profile, personalized, fuzzy, synonyms):

    should_queryset = []
    must_queryset = []

    interest = ""
    language = ""
    fuzzyness_value = ""
    synonyms_value = ""
    prefix_value = 0

    if fuzzy:
        fuzzyness_value = "AUTO"
        prefix_value = 2
    else:
        fuzzyness_value = "0"

    if synonyms:
        synonyms_value = "true"
    else:
        synonyms_value = "false"

    items = []

   

    if personalized :
        interest = Profile.get_genre_preferences(profile)
        language = Profile.get_language(profile)

        should_queryset = [
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
        ]

    if query_text :
        must_queryset = [
            Q({"multi_match":                                       # Query type
                    {"query": query_text, 
                    "fields": ['title^2', 'overview'],              # Boosting results in the title field compared to the overview field
                    "fuzziness": fuzzyness_value,                            # Lets search for words with typos in them
                    "prefix_length": prefix_value,
                    "auto_generate_synonyms_phrase_query": synonyms_value,  # Generates words synonims if possible in the query (ny = new and york)
                    "type": "best_fields",
                    }
                }),
        ]
        
    query = Q(
        "bool",
        must = must_queryset,         # Main query
        should = should_queryset,     # Personalization
        minimum_should_match = "20%",
        )

    items = ItemDocument.search().query(query)

    return items, interest, language