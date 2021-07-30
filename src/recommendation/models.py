from django.db import models

# Create your models here.
from django.db import models
from django.db.models import JSONField
from django.utils.text import slugify
from django.conf import settings
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from jsonfield import JSONField

def upload_location(instance, filename, **kwargs):
	file_path = 'blog/{author_id}/{title}-{filename}'.format(
			author_id=str(instance.author.id), title=str(instance.title), filename=filename
		)
	return file_path

class Recommendation(models.Model):

    sku                         = models.CharField(max_length=50, null=True, blank=True)
    artikelNr1                  = models.IntegerField(null=False, blank=True)
    artikelNr2                  = models.SmallIntegerField(null=True, blank=True)
    statusCode                  = models.IntegerField(null=True, blank=True)
    statusText                  = models.CharField(max_length=50, null=True, blank=True)

    saisonRetourenCode          = models.SmallIntegerField(null=True, blank=True)
    saisonRetourenText          = models.CharField(max_length=50, null=True, blank=True)
    saisonCode                  = models.SmallIntegerField(null=True, blank=True)
    saisonText                  = models.CharField(max_length=50, null=True, blank=True)
    geschlechtCode              = models.SmallIntegerField(null=True, blank=True)
    geschlechtText             = models.TextField(null=True, blank=True)
    rayonCode                   = models.SmallIntegerField(null=True, blank=True)
    rayonText                   = models.CharField(max_length=50, null=True, blank=True)
    warenArtCode                = models.IntegerField(null=True, blank=True)
    warenArtText                = models.CharField(max_length=50, null=True, blank=True)
    wuCode                      = models.SmallIntegerField(null=True, blank=True)
    wuText                      = models.TextField(null=True, blank=True)
    waCode                      = models.SmallIntegerField(null=True, blank=True)
    warenGruppe                 = models.CharField(max_length=50, null=True, blank=True)
    alterCode                   = models.IntegerField(null=True, blank=True)
    farbe                       = models.CharField(max_length=50, null=True, blank=True)
    material                    = models.TextField(null=True, blank=True)
    bezeichnung                 = models.TextField(null=True, blank=True)
    pictureName                 = models.TextField(null=True, blank=True)
    picturePathLocal            = models.CharField(max_length=50, null=True, blank=True)
    kollektion                  = models.TextField(null=True, blank=True)
    comCode                     = models.TextField(null=True, blank=True)
    lieferant                   = models.TextField(null=True, blank=True)
    eKchf                       = models.FloatField(null=True, blank=True)
    eti                         = models.FloatField(null=True, blank=True)
    vp                          = models.FloatField(null=True, blank=True)
    groessenCode                = models.SmallIntegerField(null=True, blank=True)
    groessen                    = models.JSONField(null=True)
    zlQty                       = models.SmallIntegerField(blank=True, null=True)
    productId                   = models.IntegerField(null=True, blank=True)
    published                   = models.BooleanField(null=True, blank=True)
    categories                  = models.JSONField(null=True)
    productName                 = models.TextField(null=True, blank=True)
    shortDescription            = models.TextField(null=True, blank=True)
    fullDescription             = models.TextField(null=True, blank=True)
    flag                        = models.TextField(null=True, blank=True)
    pictures                    = models.JSONField(null=True)
    date_published              = models.DateTimeField(auto_now_add=True, verbose_name="date published")
    date_updated                = models.DateTimeField(auto_now=True, verbose_name="date updated")
    author                      = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.sku


def pre_save_recommendation_receiever(sender, instance, *args, **kwargs):
    if not instance.sku:
        instance.sku = slugify(instance.author.username + "-" + instance.sku)

pre_save.connect(pre_save_recommendation_receiever, sender=Recommendation)