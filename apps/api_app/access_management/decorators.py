from rest_framework import status
from rest_framework.response import Response

from PokeTest.models import Group


def check_group_args(view):
    def _view(request, *args, **kwargs):
        # Gets url arguments
        pokemon_type = kwargs['pokemon_type']
        action = kwargs['action']
        # Checks the Pokemon type
        if not Group.objects.filter(name=pokemon_type):
            return Response({"message": f"{pokemon_type} is not a valid type."}, status=status.HTTP_400_BAD_REQUEST)
        # Sets list of available actions
        l_actions = ['add', 'remove']
        if action not in l_actions:
            return Response({"message": f"{action} is not a valid action."}, status=status.HTTP_400_BAD_REQUEST)

        return view(request, *args, **kwargs)

    return _view
