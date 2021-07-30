from django.conf import settings
from django_elasticsearch_dsl.documents import DocType
from django_elasticsearch_dsl_drf.compat import KeywordField, StringField
from django_elasticsearch_dsl import Document, Index, fields
from elasticsearch_dsl import analyzer, tokenizer, char_filter, token_filter
from django_elasticsearch_dsl.registries import registry
from elasticsearch_dsl.connections import connections
from rest_framework.settings import api_settings

from .models import Recommendation
from django_elasticsearch_dsl import (
    Document,
    fields,
    Index,
    Keyword,

)
# create the connection with ELASTICSEARCH server
connections.create_connection(hosts=['localhost'])

# elastic_search analyzer setup
html_strip = analyzer('html_strip',
                      tokenizer="standard",
                      filter=["lowercase", "stop", "snowball"],
                      char_filter=["html_strip"]
                      )

PUBLISHER_INDEX = Index('elastic_recommendation')


PUBLISHER_INDEX.settings(
    number_of_shards=1,
    number_of_replicas=1
)


@PUBLISHER_INDEX.doc_type
class RecommendationDocument(Document):
    class Index:
        name = 'recommendation'

    id = fields.IntegerField(attr='id')
    fielddata = True
    sku = fields.TextField(
        analyzer='snowball',
        fields={'raw':Keyword()}
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
        fields={
            'raw': {
                'type': 'keyword',
            }

        }
    )
    rayonCode = fields.ShortField(attr='rayonCode')
    rayonText = fields.TextField(
        fields={
            'raw': {
                'type': 'keyword',
            }

        }
    )
    warenArtCode = fields.IntegerField(attr='warenArtCode')
    warenArtText = fields.TextField(
        fields={
            'raw': {
                'type': 'keyword',
            }

        }
    )
    wuCode = fields.ShortField(attr='wuCode')
    wuText = fields.TextField(
        fields={
            'raw': {
                'type': 'keyword',
            }

        }
    )
    waCode = fields.ShortField(attr='waCode')
    warenGruppe = fields.TextField(
        fields={
            'raw': {
                'type': 'keyword',
            }

        }
    )
    alterCode = fields.IntegerField(attr='alterCode')
    farbe = fields.TextField(
        fields={
            'raw': {
                'type': 'keyword',
            }

        }
    )
    material = fields.TextField(
        fields={
            'raw': {
                'type': 'keyword',
            }

        }
    )
    bezeichnung = fields.TextField(
        fields={
            'raw': {
                'type': 'keyword',
            }

        }
    )
    pictureName = fields.TextField(
        fields={
            'raw': {
                'type': 'keyword',
            }

        }
    )
    picturePathLocal = fields.TextField(
        fields={
            'raw': {
                'type': 'keyword',
            }

        }
    )
    kollektion = fields.TextField(
        fields={
            'raw': {
                'type': 'keyword',
            }

        }
    )
    comCode = fields.TextField(
        fields={
            'raw': {
                'type': 'keyword',
            }

        }
    )
    lieferant = fields.TextField(
        fields={
            'raw': {
                'type': 'keyword',
            }

        }
    )
    eKchf = fields.FloatField(attr='eKchf')
    eti = fields.FloatField(attr='eti')
    vp = fields.FloatField(attr='vp')
    groessenCode = fields.FloatField(attr='groessenCode')


    groessen = fields.ObjectField()

    def prepare_groessen(self, instance):
        return instance.groessen

    categories = fields.ObjectField()
    def prepare_categories(self, instance):
        return instance.categories

    zlQty = fields.ShortField(attr='zlQty')
    productId = fields.IntegerField(attr='productId')
    published = fields.BooleanField(attr='published')

    shortDescription = fields.TextField(
        fields={
            'raw': {
                'type': 'keyword',
            }

        }
    )
    fullDescription = fields.TextField(
        fields={
            'raw': {
                'type': 'keyword',
            }

        }
    )
    flag = fields.TextField(
        analyzer=html_strip,
        fields={
            'raw': {
                'type': 'keyword',
            }

        }
    )
    date_published = fields.DateField(attr='date_published')
    date_updated = fields.DateField(attr='date_updated')
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

    ordering_param = api_settings.ORDERING_PARAM

    def get_ordering_query_params(self, request, view):
        """Get ordering query params.

        :param request: Django REST framework request.
        :param view: View.
        :type request: rest_framework.request.Request
        :type view: rest_framework.viewsets.ReadOnlyModelViewSet
        :return: Ordering params to be used for ordering.
        :rtype: list
        """
        print("fsafsd")
        query_params = request.query_params.copy()
        ordering_query_params = query_params.getlist(self.ordering_param, [])
        ordering_params_present = False
        # Remove invalid ordering query params
        for query_param in ordering_query_params:
            __key = query_param.lstrip('-')
            if __key in view.ordering_fields:
                ordering_params_present = True
                break

        # If no valid ordering params specified, fall back to `view.ordering`
        if not ordering_params_present:
            return self.get_default_ordering_params(view)

        return {}

    class Django(object):
        model = Recommendation
        fields= []