from django.urls import path
from recommendation.views import(
	create_recommendation_view,
	detail_recommendation_view,
	edit_recommendation_view,

)

app_name = 'recommendatioin'

urlpatterns = [
	path('create/', create_recommendation_view, name="create"),
	path('<sku>/', detail_recommendation_view, name="detail"),
	path('<sku>/edit', edit_recommendation_view, name="edit"),
]