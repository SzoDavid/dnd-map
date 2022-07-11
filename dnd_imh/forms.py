from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe

from dnd_imh.models import World


class WorldForm(forms.ModelForm):
    class Meta:
        model = World
        fields = ['name', 'description', 'main_map', 'max_item_tree_depth', 'max_item_tree_display_depth', 'owner']
        help_texts = {
            'max_item_tree_depth': mark_safe('Define how deep can the item relation tree get. Must be larger than 0!'),
            'max_item_tree_display_depth': mark_safe('Define how deep should the list view display the item relation '
                                                     'tree. Smaller than or equal to '
                                                     '<em>max item child tree depth</em>')
        }


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
