"""
Script creating a dataset for development stage.
Can be executed using python dataset_script.py
"""

import os
import json

import django

import requests

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PokeTest.settings')
django.setup()

from PokeTest.models import User
from PokeTest.models import Group


def set_data():
    User.objects.all().delete()
    # Creates the first user
    user = User.objects.create(username='Ash')
    user.set_password('Kanto')
    user.save()

    Group.objects.all().delete()
    # Gets all types in list pokeapi
    pokeapi_response = requests.get('https://pokeapi.co/api/v2/type/')
    d_pokeapi_response = json.loads(pokeapi_response.content)
    for result_type in d_pokeapi_response['results']:
        Group.objects.create(name=result_type['name'])


set_data()
