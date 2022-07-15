from django.urls import path

from rest_framework.authtoken.views import obtain_auth_token

from api_app.access_management import views


app_name = 'api_app'

urlpatterns = [
    path('/login/', obtain_auth_token, name='token_obtain_pair'),
    path('/group/<str:pokemon_type>/<str:action>/', views.handle_group, name='handle_group'),
    path('/user/me/', views.groups, name='groups'),
]
