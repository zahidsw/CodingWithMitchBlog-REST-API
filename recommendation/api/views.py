from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.settings import api_settings

from recommendation import ordering
from recommendation.ordering import MyCustomOrdering
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet

import json
import requests
import datetime
import pandas as pd

from django.shortcuts import render
from django.http import JsonResponse

from account.models import Account
from recommendation.models import Recommendation
from recommendation.api.serializers import RecommendationSerializer, RecommendationUpdateSerializer, \
	RecommendationCreateSerializer, RecommendationDocument, RecommendationElasicSerializer
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
	DefaultOrderingFilterBackend,
	SearchFilterBackend

)
from recommendation.utils import encoding_data

SUCCESS = 'success'
ERROR = 'error'
DELETE_SUCCESS = 'deleted'
UPDATE_SUCCESS = 'updated'
CREATE_SUCCESS = 'created'

# Response: https://gist.github.com/mitchtabian/93f287bd1370e7a1ad3c9588b0b22e3d
# Url: https://<your-domain>/api/recommendation/<sku>/
# Headers: Authorization: Token <token>
@api_view(['GET', ])
@permission_classes((IsAuthenticated, ))
def api_detail_recommendation_view(request, sku):

	try:
		recommendation = Recommendation.objects.get(sku=sku)
	except Recommendation.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	if request.method == 'GET':
		serializer = RecommendationSerializer(recommendation)
		return Response(serializer.data)


# Response: https://gist.github.com/mitchtabian/32507e93c530aa5949bc08d795ba66df
# Url: https://<your-domain>/api/blog/<slug>/update
# Headers: Authorization: Token <token>
@api_view(['PUT',])
@permission_classes((IsAuthenticated,))
def api_update_recommendation_view(request, sku):

	try:
		recommendation = Recommendation.objects.get(Sku=sku)
	except Recommendation.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	user = request.user
	if recommendation.author != user:
		return Response({'response':"You don't have permission to edit that."}) 
		
	if request.method == 'PUT':
		serializer = RecommendationUpdateSerializer(recommendation, data=request.data, partial=True)
		data = {}
		if serializer.is_valid():
			serializer.save()
			data['response'] = UPDATE_SUCCESS

			data['pk'] = recommendation.pk
			data['Sku'] = recommendation.Sku
			data['Size'] = recommendation.Size
			data['SizeKey'] = recommendation.SizeKey
			data['StatusCode'] = recommendation.StatusCode
			data['SaisonRetourenCode'] = recommendation.SaisonRetourenCode
			data['GeschlechtCode'] = recommendation.GeschlechtCode
			data['RayonCode'] = recommendation.RayonCode
			data['WarenArtCode'] = recommendation.WarenArtCode
			data['WUCode'] = recommendation.WUCode
			data['WACode'] = recommendation.WACode
			data['AlterCode'] = recommendation.AlterCode
			data['Farbe'] = recommendation.Farbe
			data['Material'] = recommendation.Material
			data['Eti'] = recommendation.Eti
			data['VP'] = recommendation.VP
			data['ZlQty'] = recommendation.ZlQty
			data['SoldOneYear'] = recommendation.SoldOneYear
			data['ShortDescription'] = recommendation.ShortDescription
			data['Categories'] = recommendation.Categories
			data['date_updated'] = recommendation.date_updated
			return Response(data=data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET',])
@permission_classes((IsAuthenticated,))
def api_is_author_of_recommendation(request, sku):
	try:
		recommendation = Recommendation.objects.get(Sku=sku)
	except Recommendation.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	data = {}
	user = request.user
	if recommendation.author != user:
		data['response'] = "You don't have permission to edit that."
		return Response(data=data)
	data['response'] = "You have permission to edit that."
	return Response(data=data)


# Response: https://gist.github.com/mitchtabian/a97be3f8b71c75d588e23b414898ae5c
# Url: https://<your-domain>/api/blog/<slug>/delete
# Headers: Authorization: Token <token>
@api_view(['DELETE',])
@permission_classes((IsAuthenticated, ))
def api_delete_recommendation_view(request, sku):

	try:
		recommendation = Recommendation.objects.get(sku=sku)
	except Recommendation.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	user = request.user
	if recommendation.author != user:
		return Response({'response':"You don't have permission to delete that."}) 

	if request.method == 'DELETE':
		operation = recommendation.delete()
		data = {}
		if operation:
			data['response'] = DELETE_SUCCESS
		return Response(data=data)


# Response: https://gist.github.com/mitchtabian/78d7dcbeab4135c055ff6422238a31f9
# Url: https://<your-domain>/api/blog/create
# Headers: Authorization: Token <token>
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def api_create_recommendation_view(request):

	if request.method == 'POST':
		data = request.data
		data['author'] = request.user.pk
		serializer = RecommendationCreateSerializer(data=data)
		data = {}
		if serializer.is_valid():
			recommendation = serializer.save()
			data['response'] = CREATE_SUCCESS
			data['pk'] = recommendation.pk
			data['Sku'] = recommendation.Sku
			data['Size'] = recommendation.Size
			data['SizeKey'] = recommendation.SizeKey
			data['statusCode'] = recommendation.statusCode
			data['SaisonRetourenCode'] = recommendation.SaisonRetourenCode
			data['GeschlechtCode'] = recommendation.GeschlechtCode
			data['RayonCode'] = recommendation.RayonCode
			data['WarenArtCode'] = recommendation.WarenArtCode
			data['WUCode'] = recommendation.WUCode
			data['WACode'] = recommendation.WACode
			data['AlterCode'] = recommendation.AlterCode
			data['Farbe'] = recommendation.Farbe
			data['Material'] = recommendation.Material
			data['Eti'] = recommendation.Eti
			data['VP'] = recommendation.VP
			data['ZlQty'] = recommendation.ZlQty
			data['SoldOneYear'] = recommendation.SoldOneYear
			data['ShortDescription'] = recommendation.ShortDescription
			data['Categories'] = recommendation.Categories
			data['date_updated'] = recommendation.date_updated
			data['username'] = recommendation.author.username
			return Response(data=data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	try:
		recommendation = Recommendation.objects.get(sku=sku)
	except Recommendation.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	if request.method == 'GET':
		serializer = RecommendationSerializer(recommendation)
		return Response(serializer.data)

# Response: https://gist.github.com/mitchtabian/78d7dcbeab4135c055ff6422238a31f9
# Url: https://<your-domain>/api/blog/create
# Headers: Authorization: Token <token>
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def api_create_recommendations_view(request):
	try:
		recommendations = Recommendation.objects.all()
		operation = recommendations.delete()
		data = {}
	except Recommendation.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)
	response = requests.get('http://localhost:8081/data.json')
	jsonList = response.json()
	serializer = {}
	if request.method == 'GET':
		for json in jsonList:
			if jsonList[-1].get('sku') == json.get('sku'):
				return Response("whole data has been downloaded")
			data = {}
			data = json
			data['author'] = request.user.pk
			serializer = RecommendationCreateSerializer(data=data)
			if serializer.is_valid():
				serializer.save()
			else:
				return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
		return Response("data=data")



# Response: https://gist.github.com/mitchtabian/ae03573737067c9269701ea662460205
# Url: 
#		1) list: https://<your-domain>/api/recommendation/list
#		2) pagination: http://<your-domain>/api/recommendation/list?page=2
#		3) search: http://<your-domain>/api/recommendation/list?search=mitch
#		4) ordering: http://<your-domain>/api/recommendation/list?ordering=-date_updated
#		4) search + pagination + ordering: <your-domain>/api/recommendation/list?search=mitch&page=2&ordering=-date_updated
# Headers: Authorization: Token <token>
class ApiRecommendationListView(ListAPIView):
	queryset = Recommendation.objects.all()
	serializer_class = RecommendationSerializer
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)
	pagination_class = PageNumberPagination
	filter_backends = (SearchFilter, OrderingFilter)
	search_fields = ('sku', 'author__username')


# Response: https://gist.github.com/mitchtabian/ae03573737067c9269701ea662460205
# Url:
#		1) list: https://<your-domain>/api/recommendation/list
#		2) pagination: http://<your-domain>/api/recommendation/list?page=2
#		3) search: http://<your-domain>/api/recommendation/list?search=mitch
#		4) ordering: http://<your-domain>/api/recommendation/list?ordering=-date_updated
#		4) search + pagination + ordering: <your-domain>/api/recommendation/list?search=mitch&page=2&ordering=-date_updated
# Headers: Authorization: Token <token>
class ApiRecommendationPredictionListView(ListAPIView):

	#recommendation = Recommendation.objects.get(sku=sku)
	#serializer = RecommendationSerializer(recommendation)
	queryset = Recommendation.objects.all()
	serializer_class = RecommendationSerializer
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)
	pagination_class = PageNumberPagination
	filter_backends = (SearchFilter, OrderingFilter)
	search_fields = ('sku', 'author__username')

# Response: https://gist.github.com/mitchtabian/93f287bd1370e7a1ad3c9588b0b22e3d
# Url: https://<your-domain>/api/recommendation/<sku>/
# Headers: Authorization: Token <token>
@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def api_prediction_recommendation_view(request, sku):

	try:
		recommendation = Recommendation.objects.get(sku=sku)
	except Recommendation.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	try:
		queryset = Recommendation.objects.all()
	except recommendation.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	if request.method == 'GET':
		serializer = RecommendationSerializer(queryset, many=True)
		return Response(serializer.data)


# Response: https://gist.github.com/mitchtabian/93f287bd1370e7a1ad3c9588b0b22e3d
# Url: https://<your-domain>/api/recommendation/<sku>/
# Headers: Authorization: Token <token>
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def api_training_recommendation_view(request, Sku):
	try:

		recommendations = Recommendation.objects.all()
	except Recommendation.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	try:
		recommendation = Recommendation.objects.filter(Sku=Sku)
		print(recommendation)
	except Recommendation.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	if request.method == 'POST':
		serializer_recommendations = RecommendationSerializer(recommendations, many=True)
		serializer_recommendation = RecommendationSerializer(recommendation)
		encoded_data = encoding_data(recommendations,recommendation)
		df_dicts = encoded_data.to_dict().values()
		return Response(df_dicts)
	return Response(recommendation.errors, status=status.HTTP_400_BAD_REQUEST)




class PublisherDocumentView(DocumentViewSet):
	document = RecommendationDocument
	serializer_class = RecommendationElasicSerializer
	lookup_field = 'id'
	fielddata = True
	filter_backends = [
		FilteringFilterBackend,
		CompoundSearchFilterBackend,
		DefaultOrderingFilterBackend,
		OrderingFilterBackend,
		SearchFilterBackend,
		SuggesterFilterBackend,  # This should be the last backend
	]

	search_fields = (
		'sku','artikelNr1','artikelNr2', 'statusCode' ,'statusText' ,'saisonRetourenCode','saisonRetourenText','saisonCode','saisonText','geschlechtCode','geschlechtText','rayonCode','rayonText','warenArtCode','warenArtText','wuCode','wuText','waCode','warenGruppe','alterCode','farbe','material','bezeichnung','pictureName','picturePathLocal','kollektion','comCode' ,'lieferant','eKchf','eti','vp','groessenCode','categories','groessen','zlQty',  'productId','published','productName','shortDescription','fullDescription','flag'
	)
	multi_match_search_fields = (
		'sku','artikelNr1','artikelNr2', 'statusCode' ,'statusText' ,'saisonRetourenCode','saisonRetourenText','saisonCode','saisonText','geschlechtCode','geschlechtText','rayonCode','rayonText','warenArtCode','warenArtText','wuCode','wuText','waCode','warenGruppe','alterCode','farbe','material','bezeichnung','pictureName','picturePathLocal','kollektion','comCode' ,'lieferant','eKchf','eti','vp','groessenCode','categories','groessen','zlQty',  'productId','published','productName','shortDescription','fullDescription','flag'
	)
	filter_fields = {
		'artikelNr1': 'artikelNr1.raw',
		'artikelNr2': 'artikelNr2.raw',
		'statusText': 'statusText.raw',
		'flag': 'flag.raw',
	}
	ordering_fields = {
		'flag': 'flag.raw',
	}
	ordering = ('-flag', )
