from django.contrib import admin

from .models import Kingdom, City, Place


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


admin.site.register(Kingdom, KingdomAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Place, PlaceAdmin)
