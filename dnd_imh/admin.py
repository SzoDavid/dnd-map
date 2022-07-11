from django.contrib import admin

from dnd_imh.models import World


class WorldAdmin(admin.ModelAdmin):
    search_fields = ['name']
    ordering = ['name']

    fieldsets = [
        ('Information', {
            'fields': ('name', 'description', 'main_map')
        }),
        ('Config', {
            'classes': ('collapse',),
            'fields': ('max_item_tree_depth', 'max_item_tree_display_depth', 'owner')
        })
    ]

    list_display = ('name', 'owner')


admin.site.register(World, WorldAdmin)
