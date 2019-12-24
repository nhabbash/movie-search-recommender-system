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
    production_companies=fields.TextField(analyzer = my_analyzer)

    class Index:
        name = 'item_index'
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0,
                    "search.slowlog.level": "trace",
                    "search.slowlog.threshold.query.trace": "0ms"}

    class Django:
        model = Item # The model associated with this Document

        # The fields of the model you want to be indexed in Elasticsearch
        fields = [
            'release_date',
            'vote_average',
            'vote_count',
            'poster_path'
        ]

# THIS PART COULD BE ADDED FROM SETTINGS IN INDEX CLASS
''',
                    'similarity': {
                        'scripted_tfidf': {
                        'type': 'scripted',
                        'script': {
                            'source': "double tf = Math.sqrt(doc.freq); double idf = Math.log((field.docCount+1.0)/(term.docFreq+1.0)) + 1.0; double norm = 1/Math.sqrt(doc.length); return query.boost * tf * idf * norm;"
                            }
                        }
                    }               
        }
        mappings = {'properties': {
                        'field': {
                        'type': 'TextField',
                        'similarity': 'scripted_tfidf'
                        }
                    }
        }
'''