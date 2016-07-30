import logging

from django.conf import settings
from django.db import models
import sendgrid

from pokewatch.pokedex.models import Pokemon


logger = logging.getLogger(__name__)


class Place(models.Model):
    label = models.CharField(unique=True, max_length=255)
    latitude = models.DecimalField(max_digits=17, decimal_places=14)
    longitude = models.DecimalField(max_digits=17, decimal_places=14)

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

    def notify(self, place, pokemon, sendgrid_client):
        logger.info(
            'Notifying %s of Pokemon nearby %s: %s.',
            self.name,
            place.label,
            ', '.join([p.name for p in pokemon]),
        )

        lines = []
        for p in pokemon:
            minutes, seconds = divmod(p.expires_in().seconds, 60)
            line = (
                'A wild {name} is nearby! '
                'It\'ll be around for {minutes} minutes and {seconds} seconds. '
                'Find it on the map at {link}.'
            ).format(
                name=p.name,
                minutes=minutes,
                seconds=seconds,
                link=p.map_link(),
            )

            lines.append(line)

        body = '\n'.join(lines)
        message = sendgrid.Mail(
            to=self.email,
            from_email=settings.FROM_EMAIL,
            subject='Pokemon near {}!'.format(place.label),
            text=body,
        )

        status, msg = self.sendgrid_client.send(message)
        log_msg = 'SendGrid returned {status}: {msg}.'.format(status=status, msg=msg)
        logger.info(log_msg) if status == 200 else logger.error(log_msg)
