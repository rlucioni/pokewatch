import json
import datetime

import requests


CENTRAL = ('42.364399098341', '-71.102836263782')


class Pokewatcher:
    pokedex_path = 'pokedex.json'
    data_url = 'https://pokevision.com/map/data/{}/{}'

    def __init__(self, coordinates):
        self.coordinates = coordinates

        self.url = self.build_url()
        self.pokedex = self.load_pokedex()
        self.nearby = self.load_nearby()

    def build_url(self):
        return self.data_url.format(*self.coordinates)

    def load_pokedex(self):
        with open(self.pokedex_path) as f:
            data = json.loads(f.read())

        return {int(k): v for k, v in data.items()}

    def load_nearby(self):
        # TODO: Timeout and other error handling. Log status.
        response = requests.get(self.url)
        data = response.json()

        return data['pokemon']

    def expires_in(self, timestamp):
        # TODO: Use Arrow?
        expiration = datetime.datetime.fromtimestamp(timestamp)
        now = datetime.datetime.now()

        return expiration - now

    def lookup(self, pokemon):
        expires_in = self.expires_in(pokemon['expiration_time'])
        name = self.pokedex[pokemon['pokemonId']]

        return name, str(expires_in)

    def refresh(self):
        self.nearby = self.load_nearby()

    def view(self):
        return [self.lookup(pokemon) for pokemon in self.nearby]
