from django.contrib import admin

from .models import Kingdom, City, Place, Terrain


class KingdomAdmin(admin.ModelAdmin):
    search_fields = ['name']
    ordering = ['name']

    list_display = ('name', 'discovered')


class CityAdmin(admin.ModelAdmin):
    search_fields = ['name', 'type']
    ordering = ['kingdom', 'name']

    list_display = ('name', 'type', 'kingdom', 'discovered')


class PlaceAdmin(admin.ModelAdmin):
    search_fields = ['name', 'type']
    ordering = ['city', 'name']

    list_display = ('name', 'type', 'city', 'discovered')


class TerrainAdmin(admin.ModelAdmin):
    fieldsets = [
        ('General', {'fields': ['name', 'pronunciation', 'type']}),
        ('Description', {'fields': ['description', 'show_description']}),
        ('Coordinates', {'fields': ['index_coords', 'kingdom_coords', 'city_coords', 'place_coords']}),
    ]
    search_fields = ['name', 'type']
    ordering = ['name']

    list_display = ('name', 'type', 'show_description')


admin.site.register(Kingdom, KingdomAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Place, PlaceAdmin)
admin.site.register(Terrain, TerrainAdmin)
