from django.contrib import admin

from pokewatch.pokewatcher.models import Place, Trainer


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    search_fields = ('label',)
    list_display = ('label', 'latitude', 'longitude')

    fields = ('label', 'latitude', 'longitude', 'created', 'modified')
    readonly_fields = ('created', 'modified')


@admin.register(Trainer)
class TrainerAdmin(admin.ModelAdmin):
    search_fields = ('name', 'email')
    list_display = ('name', 'email')

    fields = ('name', 'email', 'places', 'pokemon', 'created', 'modified')
    readonly_fields = ('created', 'modified')
