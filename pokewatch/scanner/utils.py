import datetime
import itertools

import requests

from pokewatch.pokedex.models import Pokemon


class PokeWatcher:
    """Utility for monitoring PokeVision."""
    data_url = 'https://pokevision.com/map/data/{latitude}/{longitude}'

    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude

        self.url = self.build_url()
        self.nearby = self.load_nearby()

        self.pokemon = self.dedup_nearby()

    def build_url(self):
        """
        Using the provided coordinates, construct a URL that can be used to request
        data from the PokeVision server.
        """
        return self.data_url.format(latitude=self.latitude, longitude=self.longitude)

    def load_nearby(self):
        """Load nearby Pokemon data from the PokeVision server."""
        # TODO: Timeout and other error handling. Log status.
        response = requests.get(self.url)
        data = response.json()

        # TODO: What to do when the 'status' is 'success' but the pokemon' list is empty?
        return data['pokemon']

    def dedup_nearby(self):
        """
        Return a list of unique, nearby Pokemon.

        The list is deduplicated by sorting the list of nearby Pokemon by ID and expiration
        time, then collecting adjacent elements with the same Pokemon ID. We only keep the
        first element in each group, representing the Pokemon expiring soonest.
        """
        nearby = sorted(self.nearby, key=lambda p: (p['pokemonId'], p['expiration_time']))

        pokemon = []
        for key, group in itertools.groupby(nearby, key=lambda p: p['pokemonId']):
            data = next(group)

            name = Pokemon.objects.get(pokedex_number=data['pokemonId']).name
            pokemon.append(
                NearbyPokemon(
                    name,
                    data['expiration_time'],
                    data['latitude'],
                    data['longitude'],
                )
            )

        return pokemon

    def refresh(self):
        """Update nearby Pokemon data."""
        self.nearby = self.load_nearby()
        self.pokemon = self.dedup_nearby()


class NearbyPokemon:
    """Representation of a nearby Pokemon."""
    map_url = 'https://www.google.com/maps/place/{latitude},{longitude}'

    def __init__(self, name, expiration, latitude, longitude):
        self.name = name
        self.expiration = expiration
        self.latitude = latitude
        self.longitude = longitude

    def expires_in(self):
        """Calculate time remaining until this Pokemon disappears from the map."""
        # TODO: Use Arrow?
        expiration = datetime.datetime.fromtimestamp(self.expiration)
        now = datetime.datetime.now()

        return expiration - now

    def map_link(self):
        """Return a link to Google Maps with a pin on the Pokemon's location."""
        return self.map_url.format(latitude=self.latitude, longitude=self.longitude)
