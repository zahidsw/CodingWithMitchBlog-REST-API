from django.conf import settings
from django_elasticsearch_dsl.documents import DocType
from django_elasticsearch_dsl_drf.compat import KeywordField, StringField
from django_elasticsearch_dsl import Document, Index, fields
from elasticsearch_dsl import analyzer, tokenizer, char_filter, token_filter
from django_elasticsearch_dsl.registries import registry
from elasticsearch_dsl.connections import connections
from rest_framework.settings import api_settings

from .models import SmartSearch
from django_elasticsearch_dsl import (
    Document,
    fields,
    Index,
    Keyword,

)


# elastic_search analyzer setup
html_strip = analyzer('html_strip',
                      tokenizer="standard",
                      filter=["lowercase", "stop", "snowball"],
                      char_filter=["html_strip"]
                      )

PUBLISHER_INDEX = Index('elastic_smart_search')


PUBLISHER_INDEX.settings(
    number_of_shards=1,
    number_of_replicas=1
)


@PUBLISHER_INDEX.doc_type
class SmartSearchDocument(Document):
    class Index:
        name = 'smart_search'

    id = fields.IntegerField(
        fields={'raw': Keyword()}
    )
    fielddata = True
    name = fields.TextField(
        analyzer='snowball',
        fields={'raw':Keyword()}
    )
    shortDescription = fields.TextField(
        analyzer='snowball',
        fields={'raw': Keyword()}
    )
    fullDescription = fields.TextField(
        analyzer='snowball',
        fields={'raw': Keyword()}
    )
    sku = fields.TextField(
        analyzer='snowball',
        fields={'raw':Keyword()}
    )

    stockQuantity = fields.IntegerField(
        fields={'raw':Keyword()}
    )
    price = fields.FloatField(
        fields={'raw': Keyword()}
    )
    published = fields.BooleanField(attr='published')
    oldPrice = fields.FloatField(
        fields={'raw': Keyword()}
    )

    sizeGuideUrl = fields.TextField(
        analyzer=html_strip,
        fields={
            'raw':KeywordField(),
            'suggest':fields.CompletionField(),

        }
    )
    language = fields.TextField(
        analyzer=html_strip,
        fields={
            'raw':KeywordField(),
            'suggest':fields.CompletionField(),
        }
    )
    slug = fields.TextField(
        analyzer='snowball',
        fields={'raw': Keyword()}
    )
    picture = fields.TextField(
        analyzer=html_strip,
        fields={
            'raw':KeywordField(),
            'suggest':fields.CompletionField(),

        }
    )
    sizes = fields.ObjectField(
        properties={
            'sku': StringField(
                analyzer=html_strip,
                fields={
                    'raw': KeywordField(),
                    'suggest': fields.CompletionField(),
                }
            ),
            'size': StringField(
                analyzer=html_strip,
                fields = {
                    'raw': KeywordField(),
                    'suggest': fields.CompletionField(),
                }
                                ),
            'storeId': fields.IntegerField(fields={'raw': Keyword()}),
            'stockQuantity': fields.IntegerField(fields={'raw': Keyword()}),
        }
    )
    productTags = fields.ObjectField(
        properties={
            'id': fields.IntegerField(fields={'raw': Keyword()}),
            'name': StringField(
                analyzer=html_strip,
                fields = {
                    'raw': KeywordField(),
                    'suggest': fields.CompletionField(),
                }
                                ),
            'storeId': fields.IntegerField(fields={'raw': Keyword()}),
            'stockQuantity': fields.IntegerField(fields={'raw': Keyword()}),
        }
    )
    def prepare_sizes(self, instance):
        return instance.sizes
    pictures = fields.ObjectField()

    def prepare_pictures(self, instance):
        return instance.pictures

    createdOnUtc = fields.DateField(attr='createdOnUtc')
    updatedOnUtc = fields.DateField(attr='updatedOnUtc')
    author = fields.ObjectField(
        properties={
            'username': StringField(
                fields={
                    'raw': KeywordField(),
                    'suggest': fields.CompletionField(),
                }
            ),
        }
    )

    artikelNr1 = fields.IntegerField(attr='artikelNr1')
    artikelNr2 = fields.IntegerField(attr='artikelNr2')
    statusCode = fields.ShortField(attr='statusCode')
    statusText = fields.TextField(
        analyzer=html_strip,
        fields={
            'raw':KeywordField(),
            'suggest':fields.CompletionField(),

        }
    )
    saisonRetourenCode = fields.ShortField(attr='saisonRetourenCode')
    saisonRetourenText = fields.TextField(
        fields={
            'raw':KeywordField(),

        }
    )
    saisonCode = fields.ShortField(attr='saisonCode')
    saisonText = fields.TextField(
        fields={
            'raw': {
                'type': 'keyword',
            }

        }
    )

    geschlechtCode = fields.ShortField(attr='geschlechtCode')
    geschlechtText = fields.TextField(
        fields={'raw': Keyword()}
    )
    rayonCode = fields.ShortField(attr='rayonCode')
    rayonText = fields.TextField(
        fields={'raw': Keyword()}
    )
    warenArtCode = fields.IntegerField(attr='warenArtCode')
    warenArtText = fields.TextField(
        fields={'raw': Keyword()}
    )
    wuCode = fields.ShortField(attr='wuCode')
    wuText = fields.TextField(
        fields={'raw': Keyword()}
    )
    waCode = fields.ShortField(attr='waCode')
    warenGruppe = fields.TextField(
        fields={'raw': Keyword()}
    )
    alterCode = fields.IntegerField(attr='alterCode')
    farbe = fields.TextField(
        fields={'raw': Keyword()}
    )
    material = fields.TextField(
        fields={'raw': Keyword()}
    )
    bezeichnung = fields.TextField(
        fields={'raw': Keyword()}
    )
    pictureName = fields.TextField(
        fields={'raw': Keyword()}
    )
    picturePathLocal = fields.TextField(
        fields={'raw': Keyword()}
    )
    kollektion = fields.TextField(
        fields={'raw': Keyword()}
    )
    comCode = fields.TextField(
        fields={'raw': Keyword()}
    )
    lieferant = fields.TextField(
        fields={'raw': Keyword()}
    )
    eKchf = fields.FloatField(
        fields={'raw': Keyword()}
    )


    groessenCode = fields.FloatField(
        fields={'raw': Keyword()}
    )
    productTags = fields.ObjectField(
        properties={

                    'id': fields.IntegerField(
                        fields={'raw': Keyword()}
                    ),
                    'name': StringField(
                        analyzer=html_strip,
                        fields={
                            'raw': KeywordField(),
                            'suggest': fields.CompletionField(),
                        }
                    ),


            'size': StringField(
                analyzer=html_strip,
                fields={
                    'raw': KeywordField(),
                    'suggest': fields.CompletionField(),
                }
            ),
            'storeId': fields.IntegerField(fields={'raw': Keyword()}),
            'stockQuantity': fields.IntegerField(fields={'raw': Keyword()}),
        }

    )
    def prepare_productTags(self, instance):
        return instance.productTags

    categories = fields.ObjectField(
        properties={
            'categoryRoots': fields.ObjectField(
                properties={
                    'id': fields.IntegerField(
                    fields={'raw':Keyword()}
                    ),
                    'name': StringField(
                        analyzer=html_strip,
                        fields={
                            'raw': KeywordField(),
                            'suggest': fields.CompletionField(),
                        },

                    ),
                },
            ),
            'size': StringField(
                analyzer=html_strip,
                fields={
                    'raw': KeywordField(),
                    'suggest': fields.CompletionField(),
                }
            ),
            'storeId': fields.IntegerField(fields={'raw': Keyword()}),
            'stockQuantity': fields.IntegerField(fields={'raw': Keyword()}),
        }


    )
    def prepare_categories(self, instance):
        return instance.categories


    flag = fields.TextField(
        analyzer='snowball',
        fields={'raw': Keyword()}
    )

    class Django(object):
        model = SmartSearch
        fields= []


