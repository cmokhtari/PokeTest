import json

from django.test import TestCase
from django.urls import reverse

from rest_framework import status

from PokeTest.models import User

from api_app.access_management.tests import AccessManagementMixin

HANDLE_GROUP_URL = 'api_app:access_management:handle_group'
POKEMON_DETAILS_URL = 'api_app:get_them_all:get_pokemon_details'
TEST_USER_USERNAME = 'Test'


class GetThemAllTests(TestCase, AccessManagementMixin):
    """Tests the get them all API."""
    def setUp(self):
        self.create_dataset()
        self.token = self.get_token()
        self.user = User.objects.get(username=TEST_USER_USERNAME)

    def test_get_pokemon(self):
        """Tests to read all Pokemon related to user groups"""
        # Adds group to the user
        self.client.post(
            reverse(
                HANDLE_GROUP_URL,
                kwargs={'pokemon_type': 'fire', 'action': 'add'}
            ),
            HTTP_AUTHORIZATION=self.get_token(),
        )
        # Adds group to the user
        self.client.post(
            reverse(
                HANDLE_GROUP_URL,
                kwargs={'pokemon_type': 'flying', 'action': 'add'}
            ),
            HTTP_AUTHORIZATION=self.get_token(),
        )
        # Gets all Pokemon related to the user groups
        response = self.client.get(reverse('api_app:get_them_all:get_pokemons'), HTTP_AUTHORIZATION=self.get_token())
        d_response = json.loads(response.content)
        # # Checks that the response code is 200
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Checks that we have one Charizard in the list because he is a fire and flying Pokemon.
        self.assertEqual(d_response['pokemons'].count('charizard'), 1)

    def test_get_valid_pokemon_details(self):
        """Tests to read Pokemon informations"""
        # Adds group to the user
        self.client.post(
            reverse(
                HANDLE_GROUP_URL,
                kwargs={'pokemon_type': 'fire', 'action': 'add'}
            ),
            HTTP_AUTHORIZATION=self.get_token(),
        )
        # Gets Pokemon informations
        response = self.client.get(
            reverse(POKEMON_DETAILS_URL, kwargs={'pokemon': '6'}),
            HTTP_AUTHORIZATION=self.get_token()
        )
        # # Checks that the response code is 200
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_pokemon_details(self):
        """Tests to checks Pokemon informations endpoint exceptions"""
        # Sets valid and invalid arguments to test
        invalid_pokemon_type_name = 'blastoise'
        invalid_pokemon_name = 'greymon'
        # Adds group to the user
        self.client.post(
            reverse(
                HANDLE_GROUP_URL,
                kwargs={'pokemon_type': 'fire', 'action': 'add'}
            ),
            HTTP_AUTHORIZATION=self.get_token(),
        )
        # Gets Pokemon informations
        response = self.client.get(
            reverse(POKEMON_DETAILS_URL, kwargs={'pokemon': invalid_pokemon_name}),
            HTTP_AUTHORIZATION=self.get_token()
        )
        # # Checks that the response code is 404 for an invalid Pokemon name
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Gets Pokemon informations
        response = self.client.get(
            reverse(POKEMON_DETAILS_URL, kwargs={'pokemon': invalid_pokemon_type_name}),
            HTTP_AUTHORIZATION=self.get_token()
        )
        # # Checks that the response code is 403 for an invalid Pokemon type name
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
