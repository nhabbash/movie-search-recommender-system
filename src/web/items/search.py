from django.shortcuts import render
from items.documents import ItemDocument
from elasticsearch_dsl.query import Q

def query(query_text, username):

    query = Q(
        "bool",
        must=[                          # Main query
                Q({"multi_match":                                   # Query type
                    {"query": query_text, 
                    "fields": ['title^2', 'overview'],              # Boosting results in the title field compared to the overview field
                    "fuzziness": "AUTO",                            # Lets search for words with typos in them
                    "prefix_length": 2,
                    "auto_generate_synonyms_phrase_query": "true",  # Generates words synonims if possible in the query (ny = new and york)
                    "type": "best_fields",
                    }
                })
            ],
        should=[                        # Personalization query (query expansion)
                Q({"multi_match":                                   # Query type
                    {"query": "Fantasy",                            # User genre preference
                    "fields": ['genres^4', 'overview'],             # Boosting results in the genre field compared to the overview field
                    "type": "best_fields",
                    }
                }),
                Q({"multi_match":                                   # Query type
                    {"query": "it",                                 # User language preference
                    "fields": ['spoken_lan', 'original_lan'],
                    "type": "best_fields",
                    }
                }),
            ],
        minimum_should_match = "50%", # Tries to match at least half of the should queries
        )

    items = ItemDocument.search().query(query)
    return items