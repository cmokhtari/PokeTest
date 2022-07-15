import json

from django.test import TestCase
from django.urls import reverse

import requests
from rest_framework import status

from PokeTest.models import Group
from PokeTest.models import User

GET_TOKEN_URL = 'api_app:access_management:token_obtain_pair'
HANDLE_GROUP_URL = 'api_app:access_management:handle_group'
TEST_USER_USERNAME = 'Test'
TEST_USER_PASSWORD = 'Test'


class AccessManagementMixin:
    """Utils for tests on the access management API."""

    def create_dataset(self):
        """Creates a dataset with an user and the groups."""
        # Creates the first user
        user = User.objects.create(username=TEST_USER_USERNAME)
        user.set_password(TEST_USER_PASSWORD)
        user.save()

        # Gets all types in list pokeapi
        pokeapi_response = requests.get('https://pokeapi.co/api/v2/type/')
        d_pokeapi_response = json.loads(pokeapi_response.content)
        for result_type in d_pokeapi_response['results']:
            Group.objects.create(name=result_type['name'])

        return None

    def get_token(self):
        token = self.client.post(
            reverse(GET_TOKEN_URL),
            {
                'username': TEST_USER_USERNAME,
                'password': TEST_USER_PASSWORD,
            }
        ).data.get('token')

        return f'Token {token}'


class AccessManagementTests(TestCase, AccessManagementMixin):
    """Tests the access management API."""
    def setUp(self):
        self.create_dataset()
        self.token = self.get_token()
        self.user = User.objects.get(username=TEST_USER_USERNAME)

    def test_add_group(self):
        """Tests to add a group."""
        # Sets a group name
        pokemon_type_name = 'fire'
        # Adds group to the user
        self.client.post(
            reverse(
                HANDLE_GROUP_URL,
                kwargs={'pokemon_type': pokemon_type_name, 'action': 'add'}
            ),
            HTTP_AUTHORIZATION=self.get_token(),
        )
        # Gets user groups
        l_groups = []
        for group in self.user.pokemon_groups.all():
            l_groups.append(group.name)
        # Checks that the user groups is equal to a list with the group set before
        self.assertEqual(l_groups, [pokemon_type_name])

        # Adds the same group to the user
        response = self.client.post(
            reverse(
                HANDLE_GROUP_URL,
                kwargs={'pokemon_type': pokemon_type_name, 'action': 'add'}
            ),
            HTTP_AUTHORIZATION=self.get_token(),
        )
        # Checks that we can't add a group already linked
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_remove_group(self):
        """Tests to remove a group."""
        # Sets a group name
        pokemon_type_name = 'fire'
        # Adds group to the user
        self.client.post(
            reverse(
                HANDLE_GROUP_URL,
                kwargs={'pokemon_type': pokemon_type_name, 'action': 'add'}
            ),
            HTTP_AUTHORIZATION=self.get_token(),
        )

        # Removes group from the user
        self.client.post(
            reverse(
                HANDLE_GROUP_URL,
                kwargs={'pokemon_type': pokemon_type_name, 'action': 'remove'}
            ),
            HTTP_AUTHORIZATION=self.get_token(),
        )
        # Gets user groups
        l_groups = []
        # Checks that the user groups is equal to an empty list
        self.assertEqual(l_groups, [])

        # Removes not related group from the user
        response = self.client.post(
            reverse(
                HANDLE_GROUP_URL,
                kwargs={'pokemon_type': pokemon_type_name, 'action': 'remove'}
            ),
            HTTP_AUTHORIZATION=self.get_token(),
        )
        # Checks that we can't remove a group not linked
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_group(self):
        """Tests to get user groups."""
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
                kwargs={'pokemon_type': 'ice', 'action': 'add'}
            ),
            HTTP_AUTHORIZATION=self.get_token(),
        )
        # Gets user groups
        response = self.client.get(reverse('api_app:access_management:groups'), HTTP_AUTHORIZATION=self.get_token())
        d_response = json.loads(response.content)
        # Checks that we reads the groups added before
        self.assertEqual(d_response['groups'], ['fire', 'ice'])

    def test_handle_group_decorator(self):
        """Tests to check decorator exception."""
        # Sets valid and invalid arguments to test
        invalid_pokemon_type_name = 'fake'
        valid_action = 'add'
        valid_pokemon_type_name = 'fire'
        invalid_action = 'fake'
        # Adds group to the user
        response = self.client.post(
            reverse(
                HANDLE_GROUP_URL,
                kwargs={'pokemon_type': invalid_pokemon_type_name, 'action': valid_action}
            ),
            HTTP_AUTHORIZATION=self.get_token(),
        )
        # Checks that we can't add a wrong group
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Adds group to the user
        response = self.client.post(
            reverse(
                HANDLE_GROUP_URL,
                kwargs={'pokemon_type': valid_pokemon_type_name, 'action': invalid_action}
            ),
            HTTP_AUTHORIZATION=self.get_token(),
        )
        # Checks that we can't do a wrong action for this endpoint
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
