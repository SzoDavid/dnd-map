from django.contrib import admin

from .models import Item, Coord


class ItemAdmin(admin.ModelAdmin):
    search_fields = ['name', 'type', 'parent']
    ordering = ['parent', 'type', 'name']

    fieldsets = [
        ('Information', {
            'description': 'General information of the item. If <code>discovered</code> is off, only the admin will be '
                           'able to see it',
            'fields': ('name', 'pronunciation', 'type', 'notes', 'discovered')
        }),
        ('Description', {
            'classes': ('collapse',),
            'description': 'Description of the item, which can be hidden from users by turning <i>show description</i> '
                           'off',
            'fields': ('description', 'show_description')
        }),
        ('Additional data', {
            'classes': ('collapse',),
            'fields': ('parent', 'map', 'depth')
        })
    ]

    list_display = ('name', 'parent', 'type', 'discovered', 'show_description')


class CoordAdmin(admin.ModelAdmin):
    search_fields = ['item', 'location', 'z_axis']
    ordering = ['z_axis', 'location', 'item']

    fieldsets = [
        ('Parents', {
            'description': 'Select <code>item</code> which should appear on <code>location</code>\'s map on the area '
                           'defined by <code>coords</code>. If location isn\'t set, it will appear on root level.',
            'fields': ('item', 'location')
        }),
        ('Coords', {
            'description': 'Define the area where <code>item</code> should appear. The biggest <code>z axis</code> will'
                           'appear on the top, while the lowest at the back. Default value for it is the '
                           '<code>item</code>\'s depth.',
            'fields': ('coords', 'z_axis')
        }),
    ]

    list_display = ('item', 'location', 'z_axis')


admin.site.register(Item, ItemAdmin)
admin.site.register(Coord, CoordAdmin)
