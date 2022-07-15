import json

import requests
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from api_app.access_management.access_management import get_groups

from PokeTest.views import setup_logger
# Sets the logger in a specific log file
logger = setup_logger('api_get_them_all', 'api_get_them_all.log', 102400, 1)


@api_view(['GET'])
def get_pokemons(request):
    """Returns all Pokemons related to the user group"""
    logger.info(f'{request.user.username} send a GET to reads all Pokemons related to his/her groups.')
    # Gets groups
    l_response = get_groups(request)
    # Sets the pokemon list to complete
    l_pokemon = []
    # For each groups of the user
    for group in l_response:
        logger.info(f'{request.user.username} send a GET to PokeAPI to reads the informations of {group} type.')
        # Gets the informations of the group
        pokeapi_response = requests.get(f'https://pokeapi.co/api/v2/type/{group}')
        logger.info(f'{request.user.username} received the informations of {group} type.')
        d_pokeapi_response = json.loads(pokeapi_response.content)
        # For each pokemon in the group informations
        for pokemon in d_pokeapi_response['pokemon']:
            # Adds its name on the list if its not already in
            if pokemon['pokemon']['name'] not in l_pokemon:
                l_pokemon.append(pokemon['pokemon']['name'])
    logger.info(f'{request.user.username} received all Pokemons related to his/her groups.')

    return Response({"pokemons": l_pokemon}, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_pokemon_details(request, pokemon):
    """Returns all informations related to the Pokemon"""
    logger.info(f'{request.user.username} send a GET to reads the informations of the Pokemon {pokemon}.')
    logger.info(f'{request.user.username} send a GET to PokeAPI to reads the informations of the Pokemon {pokemon}.')
    # Gets the Pokemon informations
    pokeapi_response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{pokemon}')
    logger.info(f'{request.user.username} received the informations of the Pokemon {pokemon}.')
    # Checks the Pokemon ID/Name specified in the argument
    if pokeapi_response.status_code == 404:
        logger.info(f'The Pokemon {pokemon} searched by {request.user.username} was not found.')
        return Response({"message": f"The Pokemon {pokemon} was not found."}, status=status.HTTP_404_NOT_FOUND)
    d_pokeapi_response = json.loads(pokeapi_response.content)
    # Gets groups
    l_response = get_groups(request)
    # For Pokemon types related to the Pokemon
    l_pokemon_type = []
    for pokemon_type in d_pokeapi_response['types']:
        l_pokemon_type.append(pokemon_type['type']['name'])
    # Checks if the user is allowed to see its details
    if not any(item in l_pokemon_type for item in l_response):
        logger.info(f'{request.user.username} searched the Pokemon {pokemon} but \
            he/she is not in one of a valid group.')
        message = {"message": f"You must be in one of those group {l_pokemon_type}."}
        return Response(message, status=status.HTTP_403_FORBIDDEN)

    logger.info(f'{request.user.username} received the informations of the Pokemon {pokemon}.')

    return Response(d_pokeapi_response, status=status.HTTP_200_OK)
