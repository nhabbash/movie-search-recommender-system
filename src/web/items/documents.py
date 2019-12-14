from elasticsearch_dsl import analyzer, token_filter
from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from .models import Item

my_analyzer = analyzer('my_analyzer', tokenizer = 'whitespace', filter=["lowercase", "stop", "snowball"])

@registry.register_document
class ItemDocument(Document):
    title = fields.TextField(analyzer = my_analyzer)
    overview = fields.TextField(analyzer = my_analyzer)
    original_lan = fields.TextField(analyzer = my_analyzer)
    spoken_lan = fields.TextField(analyzer = my_analyzer)
    genres = fields.TextField(analyzer = my_analyzer)

    class Index:
        name = 'item_index'
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}

    class Django:
        model = Item # The model associated with this Document

        # The fields of the model you want to be indexed in Elasticsearch
        fields = [
            'release_date'
        ]
