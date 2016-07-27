import datetime
import itertools
import json

import requests


CENTRAL = ('42.364399098341', '-71.102836263782')


class Pokewatcher:
    """Utility for monitoring PokeVision."""
    pokedex_path = 'pokedex.json'
    data_url = 'https://pokevision.com/map/data/{}/{}'

    def __init__(self, coordinates):
        self.coordinates = coordinates

        self.url = self.build_url()
        self.pokedex = self.load_pokedex()
        self.nearby = self.load_nearby()

    def build_url(self):
        """
        Using the provided coordinates, construct a URL that can be used to request
        data from the PokeVision server.
        """
        return self.data_url.format(*self.coordinates)

    def load_pokedex(self):
        """Load the Pokedex JSON from disk."""
        with open(self.pokedex_path) as f:
            data = json.loads(f.read())

        return {int(k): v for k, v in data.items()}

    def load_nearby(self):
        """Load nearby Pokemon data from the PokeVision server."""
        # TODO: Timeout and other error handling. Log status.
        response = requests.get(self.url)
        data = response.json()

        return data['pokemon']

    def refresh_nearby(self):
        """Update nearby Pokemon data by making a new request to the PokeVision server."""
        self.nearby = self.load_nearby()

    def nearby_pokemon(self):
        """
        Return a list of nearby Pokemon.

        The list of nearby Pokemon returned by the PokeVision server often
        includes several elements representing the same Pokemon. The expiration
        times on these elements are separated by less than a second. Conveniently,
        these elements seem to always be adjacent to each other in the list.

        itertools' groupby() is used here to fold those adjacent elements together.
        We then run with the first of the grouped elements, which seems to always
        be the element expiring soonest.

        Note: To fully deduplicate the nearby list, sort it by Pokemon ID first
        (and optionally, by expiration time).
        """
        pokemon = []
        for key, group in itertools.groupby(self.nearby, key=lambda p: p['pokemonId']):
            data = next(group)
            pokemon.append(
                Pokemon(self.pokedex[data['pokemonId']], data['expiration_time'])
            )

        return pokemon


class Pokemon:
    """Representation of a Pokemon."""
    def __init__(self, name, expiration):
        self.name = name
        self.expiration = expiration

    def expires_in(self):
        """Calculate time remaining until this Pokemon disappears from the map."""
        # TODO: Use Arrow?
        expiration = datetime.datetime.fromtimestamp(self.expiration)
        now = datetime.datetime.now()

        return expiration - now
