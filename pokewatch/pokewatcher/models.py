from django.db import models

from pokewatch.pokedex.models import Pokemon


class Place(models.Model):
    label = models.CharField(unique=True, max_length=255)
    latitude = models.DecimalField(max_digits=16, decimal_places=14)
    longitude = models.DecimalField(max_digits=16, decimal_places=14)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta(object):
        ordering = ['label']
        unique_together = ('latitude', 'longitude')
        index_together = ('latitude', 'longitude')

    def __str__(self):
        return self.label


class Trainer(models.Model):
    name = models.CharField(unique=True, max_length=255)
    email = models.EmailField(unique=True)

    places = models.ManyToManyField(Place, related_name='trainers')
    pokemon = models.ManyToManyField(Pokemon, related_name='trainers')

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta(object):
        ordering = ['name']

    def __str__(self):
        return self.name
