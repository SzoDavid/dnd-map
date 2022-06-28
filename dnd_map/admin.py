from django.contrib import admin

from .models import Kingdom, City, Place, Terrain, TerrainCoords


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
    ]
    search_fields = ['name', 'type']
    ordering = ['name']

    list_display = ('name', 'type', 'show_description')


class TerrainCoordsAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['terrain', 'location', 'coords']}),
        ('Parent (Select one in "Location")', {'fields': ['kingdom', 'city']}),
    ]
    search_fields = ['terrain', 'location', 'kingdom', 'city']
    list_display = ('terrain', 'location', 'kingdom', 'city')


admin.site.register(Kingdom, KingdomAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Place, PlaceAdmin)
admin.site.register(Terrain, TerrainAdmin)
admin.site.register(TerrainCoords, TerrainCoordsAdmin)
