import datetime
import itertools
import json

import requests


class PokeWatcher:
    """Utility for monitoring PokeVision."""
    pokedex_path = 'pokedex.json'
    data_url = 'https://pokevision.com/map/data/{}/{}'

    def __init__(self, coordinates):
        self.coordinates = coordinates

        self.url = self.build_url()
        self.nearby = self.load_nearby()
        self.pokedex = self.load_pokedex()

        self.pokemon = self.dedup_nearby()

    def build_url(self):
        """
        Using the provided coordinates, construct a URL that can be used to request
        data from the PokeVision server.
        """
        return self.data_url.format(*self.coordinates)

    def load_nearby(self):
        """Load nearby Pokemon data from the PokeVision server."""
        # TODO: Timeout and other error handling. Log status.
        response = requests.get(self.url)
        data = response.json()

        # TODO: What to do when the 'status' is 'success' but the pokemon' list is empty?
        return data['pokemon']

    def load_pokedex(self):
        """Load the Pokedex JSON from disk."""
        with open(self.pokedex_path) as f:
            data = json.loads(f.read())

        return {int(k): v for k, v in data.items()}

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
            pokemon.append(
                Pokemon(self.pokedex[data['pokemonId']], data['expiration_time'])
            )

        return pokemon

    def refresh(self):
        """Update nearby Pokemon data."""
        self.nearby = self.load_nearby()
        self.pokemon = self.dedup_nearby()


class Pokemon:
    """Representation of a Pokemon."""
    def __init__(self, name, expiration):
        # TODO: Store coordinates, too.
        self.name = name
        self.expiration = expiration

    def expires_in(self):
        """Calculate time remaining until this Pokemon disappears from the map."""
        # TODO: Use Arrow?
        expiration = datetime.datetime.fromtimestamp(self.expiration)
        now = datetime.datetime.now()

        return expiration - now
