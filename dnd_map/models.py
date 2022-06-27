from django.db import models


class Kingdom(models.Model):
    name = models.CharField(max_length=64)
    pronunciation = models.CharField(max_length=64, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    map = models.ImageField(upload_to='maps/kingdoms', blank=True, null=True)
    coords = models.CharField(max_length=19, blank=True, null=True)
    discovered = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=64)
    pronunciation = models.CharField(max_length=64, blank=True, null=True)
    kingdom = models.ForeignKey(Kingdom, on_delete=models.CASCADE)
    type = models.CharField(max_length=64, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    map = models.ImageField(upload_to='maps/cities', blank=True, null=True)
    index_coords = models.CharField(max_length=19, blank=True, null=True)
    kingdom_coords = models.CharField(max_length=19, blank=True, null=True)
    discovered = models.BooleanField(default=False)
    capital = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "cities"

    def __str__(self):
        return self.name


class Place(models.Model):
    name = models.CharField(max_length=64)
    pronunciation = models.CharField(max_length=64, blank=True, null=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    type = models.CharField(max_length=64, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    map = models.ImageField(upload_to='maps/places', blank=True, null=True)
    index_coords = models.CharField(max_length=19, blank=True, null=True)
    kingdom_coords = models.CharField(max_length=19, blank=True, null=True)
    city_coords = models.CharField(max_length=19, blank=True, null=True)
    discovered = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Terrain(models.Model):
    name = models.CharField(max_length=64)
    pronunciation = models.CharField(max_length=64, blank=True, null=True)
    type = models.CharField(max_length=64, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    show_description = models.BooleanField(default=False)
    index_coords = models.CharField(max_length=19, blank=True, null=True)
    kingdom_coords = models.CharField(max_length=19, blank=True, null=True)
    city_coords = models.CharField(max_length=19, blank=True, null=True)
    place_coords = models.CharField(max_length=19, blank=True, null=True)

    def __str__(self):
        return self.name
