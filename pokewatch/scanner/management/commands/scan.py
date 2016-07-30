import json
import logging

from django.conf import settings
from django.core.management.base import BaseCommand
import sendgrid

from pokewatch.scanner.models import Place, Trainer
from pokewatch.scanner.utils import PokeWatcher


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Scan for Pokemon.'

    def handle(self, *args, **options):
        sendgrid_client = sendgrid.SendGridClient(
            settings.SENDGRID_USERNAME,
            settings.SENDGRID_PASSWORD,
        )

        for place in Place.objects.all():
            logger.info('Scanning %s', place.label)

            watcher = PokeWatcher(place.latitude, place.longitude)

            for trainer in Trainer.objects.all():
                if place in trainer.places.all():
                    logger.info('%s is interested in Pokemon near %s, checking wishlist.', trainer.name, place.label)

                    wishlist = [p.name for p in trainer.pokemon.all()]
                    pokemon = [p for p in watcher.pokemon if p.name in wishlist]

                    if pokemon:
                        trainer.notify(place, pokemon, sendgrid_client)
