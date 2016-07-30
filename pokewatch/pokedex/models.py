from django.contrib.postgres.fields import JSONField
from django.db import models


class Pokemon(models.Model):
    name = models.CharField(unique=True, max_length=255)
    pokedex_number = models.PositiveIntegerField(unique=True)

    sightings = JSONField(default=list)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta(object):
        ordering = ['name']
        verbose_name_plural = 'pokemon'

    def __str__(self):
        return self.name
