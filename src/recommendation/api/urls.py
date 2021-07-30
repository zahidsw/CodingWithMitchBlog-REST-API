from django.urls import path
from recommendation.api.views import(
	api_detail_recommendation_view,
	api_update_recommendation_view,
	api_delete_recommendation_view,
	api_create_recommendation_view,
	api_is_author_of_recommendation,
	ApiRecommendationListView,
	api_prediction_recommendation_view,
	ApiRecommendationPredictionListView,
	api_training_recommendation_view,
	api_create_recommendations_view,
	PublisherDocumentView

)

app_name = 'recommendation'

urlpatterns = [
	path('<sku>/', api_detail_recommendation_view, name="detail"),
	path('<sku>/update', api_update_recommendation_view, name="update"),
	path('<sku>/delete', api_delete_recommendation_view, name="delete"),
	path('create', api_create_recommendation_view, name="create"),
	path('list', ApiRecommendationListView.as_view(), name="list"),
	path('searchelastic', PublisherDocumentView.as_view({'get': 'list'}), name="elasticfilter"),
	path('<sku>/is_author', api_is_author_of_recommendation, name="is_author"),
	path('<sku>/prediction', api_prediction_recommendation_view, name="prediction"),
	path('<Sku>/training', api_training_recommendation_view, name="training"),
	path('datafetching', api_create_recommendations_view, name="fetching"),
	path('<sku>/listpredict', ApiRecommendationPredictionListView.as_view(), name="list_prediction"),
]