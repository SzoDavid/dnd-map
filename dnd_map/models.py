from django.db import models


def discovered(item):
    if item.parent is not None:
        discovered(item.parent)
    item.discovered = True
    item.save()


def undiscovered(item):
    if item.item_set.count() != 0:
        for child in item.item_set.filter(discovered=True):
            undiscovered(child)
    item.discovered = False
    item.save()


class Item(models.Model):
    name = models.CharField(max_length=64)
    pronunciation = models.CharField(max_length=64, blank=True, null=True)
    type = models.CharField(max_length=32)
    notes = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    show_description = models.BooleanField(default=False)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    map = models.ImageField(upload_to='maps/kingdoms', blank=True, null=True)
    discovered = models.BooleanField(default=False)
    depth = models.IntegerField(default=0)

    def set_discovered(self):
        discovered(self)

    def set_undiscovered(self):
        undiscovered(self)

    class Meta:
        unique_together = ('type', 'name')
        ordering = ['name']

    def __str__(self):
        return self.name


class Coord(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='%(class)s_item')
    location = models.ForeignKey(Item, on_delete=models.CASCADE, blank=True, null=True,
                                 related_name='%(class)s_location')
    coords = models.CharField(max_length=19, blank=True, null=True)
    z_axis = models.IntegerField()

    class Meta:
        unique_together = ('item', 'location')

    def __str__(self):
        return self.coords
