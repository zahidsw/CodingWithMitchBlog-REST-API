from django.urls import path
from smartfactory.views import(
	create_smart_search_view,
	detail_smart_search_view,
	edit_smart_search_view,

)

app_name = 'smartfactory'

urlpatterns = [
	path('create/', create_smart_search_view, name="create"),
	path('<sku>/', detail_smart_search_view, name="detail"),
	path('<sku>/edit', edit_smart_search_view, name="edit"),
]