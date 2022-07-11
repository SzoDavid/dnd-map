from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
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

    def clean(self):
        cleaned_data = super().clean()
        max_item_tree_depth = cleaned_data.get('max_item_tree_depth')
        max_item_tree_display_depth = cleaned_data.get('max_item_tree_display_depth')

        if max_item_tree_depth and max_item_tree_display_depth:
            if max_item_tree_depth <= 0:
                raise ValidationError('Max item tree depth must be larger than 0!', code='invalid')
            if max_item_tree_display_depth <= 0 or max_item_tree_display_depth > max_item_tree_depth:
                raise ValidationError('Max item tree display depth must be larger than 0 and smaller than or equal to '
                                      'max item child tree depth!', code='invalid')


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
