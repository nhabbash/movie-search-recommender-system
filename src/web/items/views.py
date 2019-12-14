from django.shortcuts import render
from items.documents import ItemDocument
from elasticsearch_dsl.query import Q, MultiMatch, SF

def search(request):
    q = request.GET.get('q')

    if q:
        query = Q(
        'function_score',
        query=MultiMatch(
            fields=['title'],
            query=q
        )
    )
        items = ItemDocument.search().query(query)
    else:
        items = ""

    return render(request, 'items/search.html', {'items': items})