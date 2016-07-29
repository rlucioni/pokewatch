import json

from django.core.management.base import BaseCommand

from pokewatch.pokedex.models import Pokemon


class Command(BaseCommand):
    help = 'Load Pokedex into the database.'
    pokedex_path = 'pokewatch/pokedex/data/pokedex.json'

    def handle(self, *args, **options):
        with open(self.pokedex_path) as f:
            data = json.loads(f.read())

        for pokedex_number, name in data.items():
            Pokemon.objects.get_or_create(name=name, pokedex_number=pokedex_number)
