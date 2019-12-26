from elasticsearch_dsl import analyzer, token_filter
from elasticsearch_dsl.field import RankFeature
from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from .models import Item

standard_analyzer = analyzer('standard', tokenizer = 'standard', filter=["lowercase", "stop", "snowball"])
nostem_analyzer = analyzer('standard', tokenizer = 'standard', filter=["lowercase", "stop",])

@registry.register_document
class ItemDocument(Document):
    title = fields.TextField(analyzer = standard_analyzer)
    overview = fields.TextField(analyzer = standard_analyzer)
    original_lan = fields.TextField(analyzer = nostem_analyzer)
    spoken_lan = fields.TextField(analyzer = nostem_analyzer)
    genres = fields.TextField(analyzer = nostem_analyzer)
    production_companies = fields.TextField(analyzer = nostem_analyzer)

    class Index:
        name = 'item_index'
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0,
                    "search.slowlog.level": "trace",
                    "search.slowlog.threshold.query.trace": "0ms"}

    class Django:
        model = Item 
        
        # The fields of the model you want to be indexed in Elasticsearch
        fields = [
            'release_date',
            'vote_average',
            'vote_count',
            'weighted_vote',
            'poster_path'
        ]