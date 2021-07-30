from pandas.io.json import json_normalize
from rest_framework import status, serializers
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter, OrderingFilter
from django.conf import settings as django_settings

from django.forms.models import model_to_dict
from django_pandas.io import read_frame
import itertools
import re
from smartfactory import ordering
from smartfactory.ordering import MyCustomOrdering
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet

import json
import requests
import datetime
import pandas as pd
from django.core import serializers

from django.shortcuts import render
from django.http import JsonResponse

from account.models import Account
from smartfactory.models import SmartSearch
from smartfactory.api.serializers import SmartSearchSerializer, SmartSearchUpdateSerializer, \
	SmartSearchCreateSerializer, SmartSearchDocument, SmartSearchElasicSerializer
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet

from django_elasticsearch_dsl_drf.constants import (
    LOOKUP_FILTER_PREFIX,
    LOOKUP_FILTER_RANGE,
    LOOKUP_FILTER_TERMS,
    LOOKUP_FILTER_WILDCARD,
    LOOKUP_QUERY_EXCLUDE,
    LOOKUP_QUERY_GT,
    LOOKUP_QUERY_GTE,
    LOOKUP_QUERY_IN,
    LOOKUP_QUERY_IN,
    LOOKUP_QUERY_ISNULL,
    LOOKUP_QUERY_LT,
    LOOKUP_QUERY_LTE,
    SUGGESTER_COMPLETION,
    SUGGESTER_PHRASE,
    SUGGESTER_TERM,
)

from django_elasticsearch_dsl_drf.filter_backends import (
    FilteringFilterBackend,
    OrderingFilterBackend,
	CompoundSearchFilterBackend,
	SuggesterFilterBackend,
	DefaultOrderingFilterBackend
)
from smartfactory.utils import encoding_data, categories

SUCCESS = 'success'
ERROR = 'error'
DELETE_SUCCESS = 'deleted'
UPDATE_SUCCESS = 'updated'
CREATE_SUCCESS = 'created'

# Response: https://gist.github.com/mitchtabian/93f287bd1370e7a1ad3c9588b0b22e3d
# Url: https://<your-domain>/api/smart_search/<sku>/
# Headers: Authorization: Token <token>
@api_view(['GET', ])
@permission_classes((IsAuthenticated, ))
def api_detail_smart_search_view(request, sku):

	try:
		smart_search = SmartSearch.objects.get(sku=sku)
	except SmartSearch.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	if request.method == 'GET':
		serializer = SmartSearchSerializer(smart_search)
		return Response(serializer.data)


# Response: https://gist.github.com/mitchtabian/32507e93c530aa5949bc08d795ba66df
# Url: https://<your-domain>/api/blog/<slug>/update
# Headers: Authorization: Token <token>
@api_view(['PUT',])
@permission_classes((IsAuthenticated,))
def api_update_smart_search_view(request, sku):

	try:
		smart_search = SmartSearch.objects.get(Sku=sku)
	except SmartSearch.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	user = request.user
	if smart_search.author != user:
		return Response({'response':"You don't have permission to edit that."}) 
		
	if request.method == 'PUT':
		serializer = SmartSearchUpdateSerializer(smart_search, data=request.data, partial=True)
		data = {}
		if serializer.is_valid():
			serializer.save()
			data['response'] = UPDATE_SUCCESS

			data['pk'] = smart_search.pk
			data['Sku'] = smart_search.Sku
			data['Size'] = smart_search.Size
			data['SizeKey'] = smart_search.SizeKey
			data['StatusCode'] = smart_search.StatusCode
			data['SaisonRetourenCode'] = smart_search.SaisonRetourenCode
			data['GeschlechtCode'] = smart_search.GeschlechtCode
			data['RayonCode'] = smart_search.RayonCode
			data['WarenArtCode'] = smart_search.WarenArtCode
			data['WUCode'] = smart_search.WUCode
			data['WACode'] = smart_search.WACode
			data['AlterCode'] = smart_search.AlterCode
			data['Farbe'] = smart_search.Farbe
			data['Material'] = smart_search.Material
			data['Eti'] = smart_search.Eti
			data['VP'] = smart_search.VP
			data['ZlQty'] = smart_search.ZlQty
			data['SoldOneYear'] = smart_search.SoldOneYear
			data['ShortDescription'] = smart_search.ShortDescription
			data['Categories'] = smart_search.Categories
			data['date_updated'] = smart_search.date_updated
			return Response(data=data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET',])
@permission_classes((IsAuthenticated,))
def api_is_author_of_smart_search(request, sku):
	try:
		smart_search = SmartSearch.objects.get(Sku=sku)
	except SmartSearch.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	data = {}
	user = request.user
	if smart_search.author != user:
		data['response'] = "You don't have permission to edit that."
		return Response(data=data)
	data['response'] = "You have permission to edit that."
	return Response(data=data)


# Response: https://gist.github.com/mitchtabian/a97be3f8b71c75d588e23b414898ae5c
# Url: https://<your-domain>/api/blog/<slug>/delete
# Headers: Authorization: Token <token>
@api_view(['DELETE',])
@permission_classes((IsAuthenticated, ))
def api_delete_smart_search_view(request, sku):

	try:
		smart_search = SmartSearch.objects.get(sku=sku)
	except SmartSearch.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	user = request.user
	if smart_search.author != user:
		return Response({'response':"You don't have permission to delete that."}) 

	if request.method == 'DELETE':
		operation = smart_search.delete()
		data = {}
		if operation:
			data['response'] = DELETE_SUCCESS
		return Response(data=data)


# Response: https://gist.github.com/mitchtabian/78d7dcbeab4135c055ff6422238a31f9
# Url: https://<your-domain>/api/blog/create
# Headers: Authorization: Token <token>
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def api_create_smart_search_view(request):

	if request.method == 'POST':
		data = request.data
		data['author'] = request.user.pk
		serializer = SmartSearchCreateSerializer(data=data)
		data = {}
		if serializer.is_valid():
			smart_search = serializer.save()
			data['response'] = CREATE_SUCCESS
			data['pk'] = smart_search.id
			data['name'] = smart_search.name
			data['shortDescription'] = smart_search.shortDescription
			data['fullDescription'] = smart_search.fullDescription
			data['sku'] = smart_search.sku
			data['price'] = smart_search.price
			data['published'] = smart_search.published
			data['oldPrice'] = smart_search.oldPrice
			data['sizeGuideUrl'] = smart_search.sizeGuideUrl
			data['language'] = smart_search.language
			data['slug'] = smart_search.slug
			data['picture'] = smart_search.picture
			data['sizes'] = smart_search.sizes
			data['pictures'] = smart_search.pictures
			data['createdOnUtc'] = smart_search.createdOnUtc
			data['username'] = smart_search.author.username
			return Response(data=data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	try:
		smart_search = SmartSearch.objects.get(sku=sku)
	except SmartSearch.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	if request.method == 'GET':
		serializer = SmartSearchSerializer(smart_search)
		return Response(serializer.data)

# Response: https://gist.github.com/mitchtabian/78d7dcbeab4135c055ff6422238a31f9
# Url: https://<your-domain>/api/blog/create
# Headers: Authorization: Token <token>
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def api_create_smart_searchs_view(request):
	try:
		smart_searchs = SmartSearch.objects.all()
		operation = smart_searchs.delete()
		data = {}
	except SmartSearch.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)
	response = requests.get('http://10.0.1.5:49000/api/ErpNop')
	jsonList = response.json()
	print(len(jsonList))
	serializer = {}
	if request.method == 'GET':
		for json in jsonList:
			data = {}
			data = json
			data['author'] = request.user.pk
			serializer = SmartSearchCreateSerializer(data=data)
			if serializer.is_valid():
				serializer.save()
			else:
				return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
			if jsonList[-1].get('sku') == json.get('sku'):
				return Response("whole data has been downloaded")
		return Response("data=data")



# Response: https://gist.github.com/mitchtabian/ae03573737067c9269701ea662460205
# Url: 
#		1) list: https://<your-domain>/api/smart_search/list
#		2) pagination: http://<your-domain>/api/smart_search/list?page=2
#		3) search: http://<your-domain>/api/smart_search/list?search=mitch
#		4) ordering: http://<your-domain>/api/smart_search/list?ordering=-date_updated
#		4) search + pagination + ordering: <your-domain>/api/smart_search/list?search=mitch&page=2&ordering=-date_updated
# Headers: Authorization: Token <token>
class ApiSmartSearchListView(ListAPIView):
	queryset = SmartSearch.objects.all()
	serializer_class = SmartSearchSerializer
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)
	pagination_class = PageNumberPagination
	filter_backends = (SearchFilter, OrderingFilter)
	search_fields = ('sku', 'author__username')


# Response: https://gist.github.com/mitchtabian/ae03573737067c9269701ea662460205
# Url:
#		1) list: https://<your-domain>/api/smart_search/list
#		2) pagination: http://<your-domain>/api/smart_search/list?page=2
#		3) search: http://<your-domain>/api/smart_search/list?search=mitch
#		4) ordering: http://<your-domain>/api/smart_search/list?ordering=-date_updated
#		4) search + pagination + ordering: <your-domain>/api/smart_search/list?search=mitch&page=2&ordering=-date_updated
# Headers: Authorization: Token <token>
class ApiSmartSearchPredictionListView(ListAPIView):

	#smart_search = SmartSearch.objects.get(sku=sku)
	#serializer = SmartSearchSerializer(smart_search)
	queryset = SmartSearch.objects.all()
	serializer_class = SmartSearchSerializer
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)
	pagination_class = PageNumberPagination
	filter_backends = (SearchFilter, OrderingFilter)
	search_fields = ('sku', 'author__username')

# Response: https://gist.github.com/mitchtabian/93f287bd1370e7a1ad3c9588b0b22e3d
# Url: https://<your-domain>/api/smart_search/<sku>/
# Headers: Authorization: Token <token>
@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def api_prediction_smart_search_view(request, sku):

	try:
		smart_search = SmartSearch.objects.get(sku=sku)
	except SmartSearch.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	try:
		queryset = SmartSearch.objects.all()
	except smart_search.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	if request.method == 'GET':
		serializer = SmartSearchSerializer(queryset, many=True)
		return Response(serializer.data)


# Response: https://gist.github.com/mitchtabian/93f287bd1370e7a1ad3c9588b0b22e3d
# Url: https://<your-domain>/api/smart_search/<sku>/
# Headers: Authorization: Token <token>
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def api_training_smart_search_view(request, sku):
	try:
		smart_searchs = SmartSearch.objects.all()
	except SmartSearch.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	try:
		smart_search = SmartSearch.objects.filter(sku=sku)
		print(smart_search)
	except SmartSearch.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	if request.method == 'POST':
		serializer_smart_searchs = SmartSearchSerializer(smart_searchs, many=True)
		serializer_smart_search = SmartSearchSerializer(smart_search)
		encoded_data = encoding_data(smart_searchs,smart_search)
		dfdicts = encoded_data.to_dict().values()
		return Response(dfdicts)
	return Response(smart_search.errors, status=status.HTTP_400_BAD_REQUEST)


# Response: https://gist.github.com/mitchtabian/93f287bd1370e7a1ad3c9588b0b22e3d
# Url: https://<your-domain>/api/smart_search/<sku>/
# Headers: Authorization: Token <token>
@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def api_filters_value_view(request):
	newList = []
	dct = {}
	try:
		saison = SmartSearch.objects.values('saisonRetourenText').distinct()
		dct["saisonRetourenText"] = saison
		sex = SmartSearch.objects.values('geschlechtText').distinct()
		dct["geschlechtText"] = sex
		brands = SmartSearch.objects.values('kollektion').distinct()
		dct["kollektion"] = brands

		style = SmartSearch.objects.values('rayonText').distinct()
		dct["rayonText"] = style

		flag = SmartSearch.objects.values_list('flag',flat=True).distinct()
		for i in flag:
			i = i.replace(";", " ")
			newList.extend(i.split())
		seen = set()
		uniq_flag = []
		for x in newList:
			if x not in uniq_flag:
				uniq_flag.append(x)
		flag_list2 = []
		for flag in uniq_flag:
			flag_list2.append({"flag": flag})
		dct["flag"] = flag_list2

		tags = SmartSearch.objects.values_list('productTags', flat=True).distinct()
		name_list = []
		name_list2 = []
		for items in tags:
			for item in items:
				if item['name'] not in name_list:
					name_list.append(item['name'])
		for n in name_list:
			name_list2.append({"tags": n})
		dct["productTags"] = name_list2

		categories = SmartSearch.objects.values_list('categories', flat=True).distinct()
		category_list = []
		category_list2 = []
		for category in categories:
			for categy in category:
				if categy['name'] not in category_list:
					category_list.append(categy['name'])
				index =0
				for cat in categy['categoryRoots']:
					if(index>0):
						if cat['name'] not in category_list:
							category_list.append(cat['name'])
					else:
						index = 1
		for n in category_list:
			category_list2.append({"category": n})
		dct["categories"] = category_list2

		#dct["categories"] = categories(read_frame(SmartSearch.objects.values_list('categories', flat=True).distinct())[['categories']])
		return Response(dct)
	except SmartSearch.DoesNotExist :
		return Response(status=status.HTTP_404_NOT_FOUND)


class PublisherDocumentView(DocumentViewSet):
	print(DocumentViewSet)
	print((django_settings.REST_FRAMEWORK)['PAGE_SIZE'])
	document = SmartSearchDocument
	serializer_class = SmartSearchElasicSerializer
	lookup_field = 'id'
	fielddata = True
	filter_backends = [
		FilteringFilterBackend,
		CompoundSearchFilterBackend,
		DefaultOrderingFilterBackend,
		OrderingFilterBackend,
		SuggesterFilterBackend,  # This should be the last backend
	]

	search_fields = (
		'name',
		'shortDescription',
		'fullDescription',
		'sku',
		'stockQuantity',
		'price',
		'published',
		'oldPrice',
		'sizeGuideUrl',
		'language',
		'slug',
		'picture',
		'sizes.size',
		'pictures',
		'createdOnUtc',
		'updatedOnUtc',
		'author',
		'artikelNr1',
		'artikelNr2',
		'statusCode',
		'statusText',
		'saisonRetourenCode',
		'saisonRetourenText',
		'saisonCode',
		'saisonText',
		'geschlechtCode',
		'geschlechtText',
		'rayonCode',
		'rayonText',
		'warenArtCode',
		'warenArtText',
		'wuCode',
		'wuText',
		'waCode',
		'warenGruppe',
		'alterCode',
		'farbe',
		'material',
		'bezeichnung',
		'pictureName',
		'picturePathLocal',
		'kollektion',
		'comCode',
		'lieferant',
		'eKchf',
		'groessenCode',
		'categories.categoryRoots.name',
		'productTags.name'
		'published',
		'flag',
	)

	multi_match_search_fields = (
		'id','name', 'shortDescription', 'fullDescription', 'sku', 'stockQuantity', 'price', 'published', 'oldPrice','sizeGuideUrl', 'language', 'slug', 'picture', 'sizes', 'pictures', 'createdOnUtc', 'updatedOnUtc', 'author','artikelNr1', 'artikelNr2', 'statusCode', 'statusText', 'saisonRetourenCode', 'saisonRetourenText','saisonCode', 'saisonText', 'geschlechtCode', 'geschlechtText', 'rayonCode', 'rayonText', 'warenArtCode','warenArtText', 'wuCode', 'wuText', 'waCode', 'warenGruppe', 'alterCode', 'farbe', 'material', 'bezeichnung','pictureName', 'picturePathLocal', 'kollektion', 'comCode', 'lieferant', 'eKchf', 'groessenCode','categories', 'published', 'shortDescription', 'fullDescription', 'productTags','flag',
	)
	filter_fields = {
		'id':None,
		'name': 'name.raw',
		'shortDescription'	: 'shortDescription.raw',
		'fullDescription'	: 'fullDescription.raw',
		'sku': 'sku.raw',
		'stockQuantity': 'stockQuantity.raw',
		'price': 'price.raw',
		'published': 'published.raw',
		'oldPrice': 'oldPrice.raw',
		'sizeGuideUrl': 'sizeGuideUrl.raw',
		'language': 'language.raw',
		'slug': 'slug.raw',
		'picture': 'picture.raw',
		'sizes': 'sizes.size.raw',
		'pictures': 'pictures.raw',
		'categories': 'categories.categoryRoots.name.raw',
		'createdOnUtc': 'createdOnUtc.raw',
		'updatedOnUtc': 'updatedOnUtc.raw',
		'flag': 'flag.raw',
		'productTags':'productTags.name.raw'
	}
	ordering_fields = {
		'createdOnUtc': 'createdOnUtc',
		'updatedOnUtc': 'updatedOnUtc',
	}
	ordering = ('-createdOnUtc', )
