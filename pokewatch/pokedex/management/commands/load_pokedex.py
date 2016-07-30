import json
import logging

from django.core.management.base import BaseCommand

from pokewatch.pokedex.models import Pokemon


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Load Pokedex into the database.'
    pokedex_path = 'pokewatch/pokedex/data/pokedex.json'

    def add_arguments(self, parser):
        parser.add_argument(
            '-o', '--originals',
            action='store_true',
            dest='originals',
            default=False,
            help='Only load the original 151 Pokemon.'
        )

    def handle(self, *args, **options):
        originals = options.get('originals')

        with open(self.pokedex_path) as f:
            data = json.load(f)

        for pokedex_number, name in data.items():
            pokedex_number = int(pokedex_number)

            if (originals and pokedex_number <= 151) or (not originals):
                _, created = Pokemon.objects.get_or_create(name=name, pokedex_number=pokedex_number)

                if created:
                    logger.info('Saved %s: %s', pokedex_number, name)
