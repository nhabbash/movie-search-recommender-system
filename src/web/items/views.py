from django.shortcuts import render
from items.documents import ItemDocument
from elasticsearch_dsl.query import Q, MultiMatch, SF, Bool
from elasticsearch_dsl import query
from .models import Consumer

def search(request):
    q = request.GET.get('q')
    user = request.GET.get('u')
    
    if q:
        if user == "":
            query = Q(
                'function_score',
                query=MultiMatch(
                    fields=['title'],
                    query=q
                )
            )
            items = ItemDocument.search().query(query)
        else:
            interest = Consumer.get_interest(user)
            d = {
                "bool": {
                    "should": {"term": {"genres": 'Science Fiction'}},
                    "minimum_should_match" : 1
                }
            }
            query = Q(d)
            items = ItemDocument.search().query(query)

    else:
        items = ""

    return render(request, 'items/search.html', {'items': items})