from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Load Pokedex into the database.'

    def handle(self, *args, **options):
        pass
