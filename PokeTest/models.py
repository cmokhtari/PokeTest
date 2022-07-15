from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pokemon_groups = models.ManyToManyField(
        'PokeTest.Group',
        related_name='user_group',
    )


class Group(models.Model):
    """
    It represents a pokemon group.
    """
    name = models.CharField(max_length=50, unique=True)
