from elasticsearch_dsl import document
from rest_framework import serializers
from smartfactory.models import SmartSearch
from django_elasticsearch_dsl_drf.serializers import DocumentSerializer
from smartfactory.documents import SmartSearchDocument
import os
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.storage import FileSystemStorage
from smartfactory.utils import is_image_aspect_ratio_valid, is_image_size_valid


class SmartSearchSerializer(serializers.ModelSerializer):

	username = serializers.SerializerMethodField('get_username_from_author')

	class Meta:
		model = SmartSearch
		fields = ['id','name','shortDescription', 'fullDescription' ,'sku' ,'stockQuantity','price','published','oldPrice','sizeGuideUrl','language','slug','picture','sizes','pictures','createdOnUtc','updatedOnUtc','author','artikelNr1', 'artikelNr2', 'statusCode', 'statusText', 'saisonRetourenCode', 'saisonRetourenText','saisonCode', 'saisonText', 'geschlechtCode', 'geschlechtText', 'rayonCode', 'rayonText', 'warenArtCode','warenArtText', 'wuCode', 'wuText', 'waCode', 'warenGruppe', 'alterCode', 'farbe', 'material', 'bezeichnung','pictureName', 'picturePathLocal', 'kollektion', 'comCode', 'lieferant', 'eKchf', 'eti', 'vp', 'groessenCode','categories', 'groessen', 'zlQty', 'published','flag','username']


	def get_username_from_author(self, smartfactory):
		username = smartfactory.author.username
		return username

class SmartSearchUpdateSerializer(serializers.ModelSerializer):
	groessen = serializers.JSONField()
	categories = serializers.JSONField()
	class Meta:
		model = SmartSearch
		fields = ['id','name','shortDescription', 'fullDescription' ,'sku' ,'stockQuantity','price','published','oldPrice','sizeGuideUrl','language','slug','picture','sizes','pictures','createdOnUtc','updatedOnUtc','author','artikelNr1', 'artikelNr2', 'statusCode', 'statusText', 'saisonRetourenCode', 'saisonRetourenText','saisonCode', 'saisonText', 'geschlechtCode', 'geschlechtText', 'rayonCode', 'rayonText', 'warenArtCode','warenArtText', 'wuCode', 'wuText', 'waCode', 'warenGruppe', 'alterCode', 'farbe', 'material', 'bezeichnung','pictureName', 'picturePathLocal', 'kollektion', 'comCode', 'lieferant', 'eKchf', 'eti', 'vp', 'groessenCode','categories', 'groessen', 'zlQty', 'published', 'shortDescription', 'fullDescription','flag',]

	def validate(self, smartfactory):
		try:
			pass
		except KeyError:
			pass
		return smartfactory

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

class SmartSearchJsonSerializer(serializers.Serializer):

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
	picture=serializers.IntegerField(required=False)
	slug=serializers.CharField(max_length=50)
	pictures=serializers.IntegerField()
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
		return super(SmartSearchJsonSerializer, self).validate(attrs)


class SmartSearchCreateSerializer(serializers.ModelSerializer):

	class Meta:
		model = SmartSearch
		fields = ['id','name','shortDescription', 'fullDescription' ,'sku' ,'stockQuantity','price','published','oldPrice','sizeGuideUrl','language','slug','picture','sizes','pictures','createdOnUtc','updatedOnUtc','author','artikelNr1', 'artikelNr2', 'statusCode', 'statusText', 'saisonRetourenCode', 'saisonRetourenText','saisonCode', 'saisonText', 'geschlechtCode', 'geschlechtText', 'rayonCode', 'rayonText', 'warenArtCode','warenArtText', 'wuCode', 'wuText', 'waCode', 'warenGruppe', 'alterCode', 'farbe', 'material', 'bezeichnung','pictureName', 'picturePathLocal', 'kollektion', 'comCode', 'lieferant', 'eKchf', 'groessenCode','categories', 'productTags', 'published', 'shortDescription', 'fullDescription','flag', ]

	def save(self):
		try:
			id        	 			= self.validated_data['id']
			name        	 		= self.validated_data['name']
			shortDescription 	 	= self.validated_data['shortDescription']
			fullDescription        	= self.validated_data['fullDescription']
			sku		 				= self.validated_data['sku']
			stockQuantity			= self.validated_data['stockQuantity']
			price        	 		= self.validated_data['price']
			published        	 	= self.validated_data['published']
			oldPrice    	 		= self.validated_data['oldPrice']
			sizeGuideUrl    	 	= self.validated_data['sizeGuideUrl']
			language         	 	= self.validated_data['language']
			slug         	 		= self.validated_data['slug']
			picture      	 		= self.validated_data['picture']
			sizes      	 			= self.validated_data['sizes']
			pictures            	= self.validated_data['pictures']
			createdOnUtc            = self.validated_data['createdOnUtc']
			updatedOnUtc            = self.validated_data['updatedOnUtc']

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
			groessenCode      	 = self.validated_data['groessenCode']
			productTags          = self.validated_data['productTags']
			categories        	 =self.validated_data['categories']
			flag              	 = self.validated_data['flag']


			smartfactory = SmartSearch(
				author				 	=self.validated_data['author'],
				id               	 	=id,
				name        	 	 	=name,
				shortDescription     	=shortDescription,
				fullDescription      	=fullDescription,
				sku        	 			=sku,
				stockQuantity	 		=stockQuantity,
				price	 				=price,
				published 				=published,
				oldPrice        	 	=oldPrice,
				sizeGuideUrl        	=sizeGuideUrl,
				language    	 		=language,
				slug    	 			=slug,
				picture         	 	=picture,
				sizes         	 		=sizes,
				pictures      	 		=pictures,
				createdOnUtc      	 	=createdOnUtc,
				updatedOnUtc            =updatedOnUtc,

				artikelNr1        	=artikelNr1,
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
				groessenCode      	 =groessenCode,
				productTags          =productTags,
				categories        	 =categories,
				flag              	 =flag,
				)
			smartfactory.save()
			return smartfactory
		except KeyError:
			raise serializers.ValidationError({"response": "You must have a different parameters like sku, artikelNr1 etc."})



class SmartSearchElasicSerializer(DocumentSerializer):

	class Meta:
		model = SmartSearch
		document = SmartSearchDocument
		fields = ['id','name','shortDescription', 'fullDescription' ,'sku' ,'stockQuantity','price','published','oldPrice','sizeGuideUrl','language','slug','picture','sizes','pictures','createdOnUtc','updatedOnUtc']

	def get_location(self, obj):
		"""Represent location value."""
		try:
			return obj.location.to_dict()
		except:
			return {}







