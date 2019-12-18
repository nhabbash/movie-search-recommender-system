from django.shortcuts import render
from django.http import HttpResponse
from items.documents import ItemDocument
from elasticsearch_dsl.query import Q, MultiMatch, SF, Bool
from elasticsearch_dsl import query
from .search import *

def search(request):
    q = request.GET.get('q')
    u = request.GET.get('u')
    
    if q:
        items = query(q, u)
    else:
        items = ""

    return render(request, 'items/search.html', {'items': items})

def info(request):
    print("hello")