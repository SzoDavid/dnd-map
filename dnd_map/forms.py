from django import forms

from dnd_map.models import Item, Coord


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = '__all__'


class CoordForm(forms.ModelForm):
    class Meta:
        model = Coord
        fields = '__all__'
