from elasticsearch_dsl.query import Q, MultiMatch, SF
from .documents import ItemDocument

def get_search_query(phrase):
    query = Q(
        'function_score',
        query=MultiMatch(
            fields=['overview'],
            query=phrase
        )
    )
    return ItemDocument.search().query(query)

def search(phrase):
    return get_search_query(phrase).to_queryset()

'''

    title = fields.TextField(analyzer = my_analyzer)
    overview = fields.TextField(analyzer = my_analyzer)
    original_lan = fields.TextField(analyzer = my_analyzer)
    spoken_lan = fields.TextField(analyzer = my_analyzer)
    genres = fields.TextField(analyzer = my_analyzer)
    data = fields.DateField()

'''