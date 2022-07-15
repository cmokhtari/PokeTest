from django.urls import include
from django.urls import path


app_name = 'api_app'

urlpatterns = [
    path('api', include('api_app.access_management.urls', namespace='access_management')),
    path('api/pokemon/', include('api_app.get_them_all.urls', namespace='get_them_all')),
]
