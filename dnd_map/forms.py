from django import forms
from django.utils.safestring import mark_safe

from dnd_map.models import Item, Coord


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'pronunciation', 'type', 'discovered', 'notes', 'description', 'show_description', 'parent',
                  'map']
        help_texts = {
            'name': mark_safe('[required]'),
            'type': mark_safe('[required] Classification of the item. Examples: <em>kingdom, capital, city, town,'
                              'forest, etc.</em>'),
            'discovered': mark_safe('If discovered is off, people won\'t be able to see this item, only you.'),
            'notes': mark_safe('Notes for you only'),
            'show_description': mark_safe('If show description is off, people won\'t be able to see this item\'s '
                                          'description only you.'),
            'parent': mark_safe('For example the kingdom this place is located in.'),
        }


class CoordForm(forms.ModelForm):
    class Meta:
        model = Coord
        fields = ['item', 'location', 'coords', 'z_axis']
        help_texts = {
            'item': mark_safe('[required] The item you want to appear on <em>location</em>.'),
            'location': mark_safe('[required] The item will appear on this item\'s map. If the item you want to select '
                                  'isn\'t present in the list, you may have forgot to upload its map. If nothing is '
                                  'selected, it will appear on the main map.'),
            'coords': mark_safe('[required] Specify rectangles on location\'s map by its top and bottom pixel '
                                'coordinates. When you click on that area on the map, it will redirect you on item\'s '
                                'page.<br><strong>Format:</strong> '
                                '<code>top-left-width,top-left-height,bottom-right-width,bottom-right-height</code>.'),
            'z_axis': mark_safe('[required] The biggest z axis will appear on the front, while the lowest at the back.')
        }
