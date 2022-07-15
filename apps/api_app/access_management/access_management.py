
def get_groups(request):
    """Returns groups linked to the user"""
    l_groups = []
    for group in request.user.pokemon_groups.all():
        l_groups.append(group.name)

    return l_groups
