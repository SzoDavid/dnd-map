from django.contrib import admin

from dnd_imh.models import World, Backup


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


class BackupAdmin(admin.ModelAdmin):
    search_fields = ['name', 'owner']
    ordering = ['owner', 'name']
    fieldsets = [
        ('Information', {'fields': ('name', 'owner', 'created')}),
        ('JSON', {'fields': ('data',)})
    ]

    list_display = ('name', 'owner')


admin.site.register(World, WorldAdmin)
admin.site.register(Backup, BackupAdmin)
