from django.urls import path
from smartfactory.api.views import(
	api_detail_smart_search_view,
	api_update_smart_search_view,
	api_delete_smart_search_view,
	api_create_smart_search_view,
	api_is_author_of_smart_search,
	ApiSmartSearchListView,
	api_prediction_smart_search_view,
	ApiSmartSearchPredictionListView,
	api_training_smart_search_view,
	api_create_smart_searchs_view,
	PublisherDocumentView,
	api_filters_value_view

)

app_name = 'recommendation'

urlpatterns = [
	path('<sku>/', api_detail_smart_search_view, name="detail"),
	path('<sku>/update', api_update_smart_search_view, name="update"),
	path('<sku>/delete', api_delete_smart_search_view, name="delete"),
	path('create', api_create_smart_search_view, name="create"),
	path('list', ApiSmartSearchListView.as_view(), name="list"),
	path('searchelastic', PublisherDocumentView.as_view({'get': 'list'}), name="elasticfilter"),
	path('filtersValue', api_filters_value_view, name="filtersValue"),
	path('<sku>/is_author', api_is_author_of_smart_search, name="is_author"),
	path('<sku>/prediction', api_prediction_smart_search_view, name="prediction"),
	path('<Sku>/training', api_training_smart_search_view, name="training"),
	path('datafetching', api_create_smart_searchs_view, name="fetching"),
	path('<sku>/listpredict', ApiSmartSearchPredictionListView.as_view(), name="list_prediction"),
]