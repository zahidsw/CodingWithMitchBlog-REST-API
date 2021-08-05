from elasticsearch_dsl import document
from rest_framework import serializers
from recommendation.models import Recommendation
from django_elasticsearch_dsl_drf.serializers import DocumentSerializer
from recommendation.documents import RecommendationDocument

import os
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.storage import FileSystemStorage
IMAGE_SIZE_MAX_BYTES = 1024 * 1024 * 2 # 2MB
MIN_TITLE_LENGTH = 5
MIN_BODY_LENGTH = 50

from recommendation.utils import is_image_aspect_ratio_valid, is_image_size_valid


class RecommendationSerializer(serializers.ModelSerializer):

	username = serializers.SerializerMethodField('get_username_from_author')

	class Meta:
		model = Recommendation
		fields = ['pk','sku','artikelNr1','artikelNr2', 'statusCode' ,'statusText' ,'saisonRetourenCode','saisonRetourenText','saisonCode','saisonText','geschlechtCode','geschlechtText','rayonCode','rayonText','warenArtCode','warenArtText','wuCode','wuText','waCode','warenGruppe','alterCode','farbe','material','bezeichnung','pictureName','picturePathLocal','kollektion','comCode' ,'lieferant','eKchf','eti','vp','groessenCode' ,'groessen','zlQty' ,'productId','published' ,'categories' ,'productName','shortDescription','fullDescription','flag','date_updated','username']


	def get_username_from_author(self, recommendation):
		username = recommendation.author.username
		return username

class RecommendationUpdateSerializer(serializers.ModelSerializer):
	groessen = serializers.JSONField()
	categories = serializers.JSONField()
	class Meta:
		model = Recommendation
		fields = ['sku','artikelNr1','artikelNr2', 'statusCode' ,'statusText' ,'saisonRetourenCode','saisonRetourenText','saisonCode','saisonText','geschlechtCode','geschlechtText','rayonCode','rayonText','warenArtCode','warenArtText','wuCode','wuText','waCode','warenGruppe','alterCode','farbe','material','bezeichnung','pictureName','picturePathLocal','kollektion','comCode' ,'lieferant','eKchf','eti','vp','groessenCode' ,'groessen','zlQty' ,'productId','published' ,'categories' ,'productName','shortDescription','fullDescription','flag']

	def validate(self, recommendation):
		try:
			pass
		except KeyError:
			pass
		return recommendation

class GrossenSerializer(serializers.Serializer):
    artikelNr1 = serializers.IntegerField()
    artikelNr2 = serializers.IntegerField()
    artikelGr = serializers.IntegerField()
    groessenText = serializers.CharField()
    sku = serializers.CharField()
    istZl = serializers.IntegerField()
    verkPeriode = serializers.IntegerField()

    def validate(self, attrs):
        return super(GrossenSerializer, self).validate(attrs)


class CategoriesRootsSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    parentCategoryId = serializers.IntegerField()

    def validate(self, attrs):
        return super(CategoriesRootsSerializer, self).validate(attrs)

class CategoriesSerializer(serializers.Serializer):
	id=serializers.IntegerField()
	name=serializers.CharField(max_length=50)
	parentCategoryId=serializers.IntegerField()
	categoryRoots = serializers.ListField(child=CategoriesRootsSerializer(many=True, read_only=True))

	def validate(self, attrs):
		return super(CategoriesSerializer, self).validate(attrs)

class RecommendationJsonSerializer(serializers.Serializer):

	sku=serializers.CharField(max_length=50, allow_blank=True)
	artikelNr1=serializers.IntegerField()
	artikelNr2=serializers.IntegerField()
	statusCode=serializers.IntegerField(required=False)
	statusText=serializers.CharField(max_length=50, allow_blank=True)
	saisonRetourenCode=serializers.IntegerField(required=False)
	saisonRetourenText=serializers.CharField(max_length=50, allow_blank=True)
	saisonCode=serializers.IntegerField()
	saisonText=serializers.CharField(max_length=50, allow_blank=True)
	geschlechtCode=serializers.IntegerField()
	geschlechtText=serializers.CharField(max_length=50, allow_blank=True)
	rayonCode=serializers.IntegerField(required=False)
	rayonText=serializers.CharField(max_length=50)
	warenArtCode=serializers.IntegerField()
	warenArtText=serializers.CharField(max_length=50)
	wuCode=serializers.IntegerField()
	wuText=serializers.CharField(max_length=50)
	waCode=serializers.IntegerField()
	warenGruppe=serializers.CharField(max_length=50, allow_blank=True)
	alterCode=serializers.IntegerField()
	farbe=serializers.CharField(max_length=50)
	material=serializers.CharField(max_length=50)
	bezeichnung=serializers.CharField(max_length=50)
	pictureName=serializers.CharField(max_length=50)
	picturePathLocal=serializers.CharField(max_length=50)
	kollektion=serializers.CharField(max_length=50, allow_blank=True)
	comCode=serializers.CharField(max_length=50)
	lieferant=serializers.CharField(max_length=50)
	eKchf=serializers.FloatField()
	eti=serializers.FloatField()
	vp=serializers.FloatField()
	groessenCode=serializers.IntegerField()
	groessen=GrossenSerializer(many=True,  read_only=True)

	zlQty=serializers.IntegerField()
	productId=serializers.IntegerField()
	published=serializers.BooleanField()
	categories=CategoriesSerializer(many=True, read_only=True)
	productName=serializers.CharField(max_length=50)
	shortDescription=serializers.CharField(max_length=150)
	fullDescription=serializers.CharField()
	flag=serializers.CharField(allow_blank=True)
	def validate(self, attrs):
		return super(RecommendationJsonSerializer, self).validate(attrs)


class RecommendationCreateSerializer(serializers.ModelSerializer):

	class Meta:
		model = Recommendation
		fields = ['sku','artikelNr1','artikelNr2', 'statusCode' ,'statusText' ,'saisonRetourenCode','saisonRetourenText','saisonCode','saisonText','geschlechtCode','geschlechtText','rayonCode','rayonText','warenArtCode','warenArtText','wuCode','wuText','waCode','warenGruppe','alterCode','farbe','material','bezeichnung','pictureName','picturePathLocal','kollektion','comCode' ,'lieferant','eKchf','eti','vp','groessenCode','categories','groessen','zlQty',  'productId','published','productName','shortDescription','fullDescription','flag','pictures','author']

	def save(self):
		try:
			sku               	 = self.validated_data['sku']
			artikelNr1        	 = self.validated_data['artikelNr1']
			artikelNr2        	 = self.validated_data['artikelNr2']
			statusCode        	 = self.validated_data['statusCode']
			statusText        	 = self.validated_data['statusText']
			saisonRetourenCode	 = self.validated_data['saisonRetourenCode']
			saisonRetourenText	 = self.validated_data['saisonRetourenText']
			saisonCode        	 = self.validated_data['saisonCode']
			saisonText        	 = self.validated_data['saisonText']
			geschlechtCode    	 = self.validated_data['geschlechtCode']
			geschlechtText    	 = self.validated_data['geschlechtText']
			rayonCode         	 = self.validated_data['rayonCode']
			rayonText         	 = self.validated_data['rayonText']
			warenArtCode      	 = self.validated_data['warenArtCode']
			warenArtText      	 = self.validated_data['warenArtText']
			wuCode            	 = self.validated_data['wuCode']
			wuText            	 = self.validated_data['wuText']
			waCode            	 = self.validated_data['waCode']
			warenGruppe       	 = self.validated_data['warenGruppe']
			alterCode         	 = self.validated_data['alterCode']
			farbe             	 = self.validated_data['farbe']
			material          	 = self.validated_data['material']
			bezeichnung       	 = self.validated_data['bezeichnung']
			pictureName       	 = self.validated_data['pictureName']
			picturePathLocal  	 = self.validated_data['picturePathLocal']
			kollektion        	 = self.validated_data['kollektion']
			comCode           	 = self.validated_data['comCode']
			lieferant         	 = self.validated_data['lieferant']
			eKchf             	 = self.validated_data['eKchf']
			eti               	 = self.validated_data['eti']
			vp                	 = self.validated_data['vp']
			groessenCode      	 = self.validated_data['vp']
			groessen          	 = self.validated_data['groessen']
			zlQty             	 = self.validated_data['zlQty']
			productId         	 = self.validated_data['productId']
			published         	 = self.validated_data['published']
			categories        	 =self.validated_data['categories']
			productName       	 = self.validated_data['productName']
			shortDescription  	 = self.validated_data['shortDescription']
			fullDescription   	 = self.validated_data['fullDescription']
			flag              	 = self.validated_data['flag']
			pictures 			 = self.validated_data['pictures']

			recommendation = Recommendation(
				author				 =self.validated_data['author'],
				sku               	 =sku,
				artikelNr1        	 =artikelNr1,
				artikelNr2        	 =artikelNr2,
				statusCode        	 =statusCode,
				statusText        	 =statusText,
				saisonRetourenCode	 =saisonRetourenCode,
				saisonRetourenText	 =saisonRetourenText,
				saisonCode        	 =saisonCode,
				saisonText        	 =saisonText,
				geschlechtCode    	 =geschlechtCode,
				geschlechtText    	 =geschlechtText,
				rayonCode         	 =rayonCode,
				rayonText         	 =rayonText,
				warenArtCode      	 =warenArtCode,
				warenArtText      	 =warenArtText,
				wuCode            	 =wuCode,
				wuText            	 =wuText,
				waCode            	 =waCode,
				warenGruppe       	 =warenGruppe,
				alterCode         	 =alterCode,
				farbe             	 =farbe,
				material          	 =material,
				bezeichnung       	 =bezeichnung,
				pictureName       	 =pictureName,
				picturePathLocal  	 =picturePathLocal,
				kollektion        	 =kollektion,
				comCode           	 =comCode,
				lieferant         	 =lieferant,
				eKchf             	 =eKchf,
				eti               	 =eti,
				vp                	 =vp,
				groessenCode      	 =groessenCode,
				groessen          	 =groessen,
				zlQty             	 =zlQty,
				productId         	 =productId,
				published         	 =published,
				categories        	 =categories,
				productName       	 =productName,
				shortDescription  	 =shortDescription,
				fullDescription   	 =fullDescription,
				flag              	 =flag,
				pictures			 =pictures
				)
			recommendation.save()
			return recommendation
		except KeyError:
			raise serializers.ValidationError({"response": "You must have a different parameters like sku, artikelNr1 etc."})



class RecommendationElasicSerializer(DocumentSerializer):

	class Meta:
		model = Recommendation
		document = RecommendationDocument
		fields = ['sku','artikelNr1','artikelNr2', 'statusCode' ,'statusText' ,'saisonRetourenCode','saisonRetourenText','saisonCode','saisonText','geschlechtCode','geschlechtText','rayonCode','rayonText','warenArtCode','warenArtText','wuCode','wuText','waCode','warenGruppe','alterCode','farbe','material','bezeichnung','pictureName','picturePathLocal','kollektion','comCode' ,'lieferant','eKchf','eti','vp','groessenCode','categories','groessen','zlQty',  'productId','published','productName','shortDescription','fullDescription','flag','pictures','author']

	def get_location(self, obj):
		"""Represent location value."""
		try:
			return obj.location.to_dict()
		except:
			return {}







