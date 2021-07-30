from django.contrib import admin

from .models import *
@admin.register(Recommendation)
class RecommendationAdmin(admin.ModelAdmin):
    """Book admin."""

    list_display = ('sku', 'artikelNr1', 'shortDescription', 'fullDescription')
    search_fields = ('sku',)

