from django.contrib import admin

from pokewatch.pokedex.models import Pokemon


@admin.register(Pokemon)
class PokemonAdmin(admin.ModelAdmin):
    search_fields = ('name', 'pokedex_number')
    list_display = ('name', 'pokedex_number')

    fields = ('name', 'pokedex_number', 'created', 'modified')
    readonly_fields = ('name', 'pokedex_number', 'created', 'modified')
