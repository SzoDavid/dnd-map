from django.db import models


class Kingdom(models.Model):
    name = models.CharField(max_length=64)
    pronunciation = models.CharField(max_length=64, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    map_path = models.CharField(max_length=32, blank=True, null=True)
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
    map_path = models.CharField(max_length=32, blank=True, null=True)
    coords = models.CharField(max_length=19, blank=True, null=True)
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
    map_path = models.CharField(max_length=32, blank=True, null=True)
    coords = models.CharField(max_length=19, blank=True, null=True)
    discovered = models.BooleanField(default=False)

    def __str__(self):
        return self.name
