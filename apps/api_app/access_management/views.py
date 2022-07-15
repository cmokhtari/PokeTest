
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api_app.access_management.decorators import check_group_args
from PokeTest.models import Group
from PokeTest.models import User

from PokeTest.views import setup_logger
# Sets the logger in a specific log file
logger = setup_logger('api_access_management', 'api_access_management.log', 102400, 1)


@api_view(['POST'])
@check_group_args
def handle_group(request, pokemon_type, action):
    """
    Group can be handle with the following actions.
    add: Add the specified group to the user
    remove: Remove the specified group from the user
    """
    logger.info(f'{request.user.username} send a POST to {action} the {pokemon_type} group.')
    # Gets the group related to the Pokemon type
    group = Group.objects.get(name=pokemon_type)
    # Gets user
    user = User.objects.get(id=request.user.id)

    if action == 'add':
        # Checks if the group was already added
        if group in user.pokemon_groups.all():
            logger.info(f'{request.user.username} is already in the {pokemon_type} group.')
            message = {"message": f"You are already in the {pokemon_type} group."}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        else:
            user.pokemon_groups.add(group)
            logger.info(f'The {pokemon_type} group has been added to {request.user.username}.')
    elif action == 'remove':
        # Checks if the group was set
        if group not in user.pokemon_groups.all():
            logger.info(f'{request.user.username} is not in the {pokemon_type} group.')
            message = {"message": f"You are not in the {pokemon_type} group."}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        else:
            user.pokemon_groups.remove(group)
            logger.info(f'The {pokemon_type} group has been removed to {request.user.username}.')

    return Response(status=status.HTTP_201_CREATED)


@api_view(['GET'])
def groups(request):
    """Returns the groups linked to the user."""
    logger.info(f'{request.user.username} send a GET to reads his/her group.')
    # Gets user
    user = User.objects.get(id=request.user.id)
    # Sets the groups list
    l_groups = []
    # For each groups linked to user
    for group in user.pokemon_groups.all():
        # Adds the group to the list
        l_groups.append(group.name)
    logger.info(f'{request.user.username} received his/her groups.')

    return Response({"groups": l_groups}, status=status.HTTP_200_OK)
