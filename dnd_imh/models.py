from django.db import models
from django.contrib.auth.models import User


class World(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField(blank=True, null=True)
    main_map = models.ImageField(upload_to='maps', blank=True, null=True)
    max_item_tree_depth = models.IntegerField(default=5)
    max_item_tree_display_depth = models.IntegerField(default=5)
    owner = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name
