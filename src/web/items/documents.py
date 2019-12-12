from elasticsearch_dsl import analyzer
from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from .models import Item

my_analyzer = analyzer('my_analyzer', tokenizer="standard", filter=["lowercase", "stop", "snowball"])

@registry.register_document
class ItemDocument(Document):
    #title = fields.TextField(analyzer = my_analyzer)
    overview = fields.TextField(analyzer = my_analyzer)
    original_lan = fields.TextField(analyzer = my_analyzer)
    spoken_lan = fields.TextField(analyzer = my_analyzer)
    genres = fields.TextField(analyzer = my_analyzer)
    date = fields.DateField()

    class Index:
        name = 'item_index'
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}

    class Django:
        model = Item # The model associated with this Document

        # The fields of the model you want to be indexed in Elasticsearch
        '''fields = [
            'title',
            'overview',
            'original_lan',
            'spoken_lan',
            'genres',
        ]'''
        fields = ['title']