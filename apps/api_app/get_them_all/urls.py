from django.urls import path

from api_app.get_them_all import views


app_name = 'api_app'

urlpatterns = [
    path('', views.get_pokemons, name='get_pokemons'),
    path('<str:pokemon>/', views.get_pokemon_details, name='get_pokemon_details'),
]
