from django import forms

from dnd_map.models import Kingdom, City, Place


class KingdomForm(forms.ModelForm):
    class Meta:
        # To specify the model to be used to create form
        model = Kingdom
        # It includes all the fields of model
        fields = '__all__'


class CityForm(forms.ModelForm):
    class Meta:
        # To specify the model to be used to create form
        model = City
        # It includes all the fields of model
        fields = '__all__'


class PlaceForm(forms.ModelForm):
    class Meta:
        # To specify the model to be used to create form
        model = Place
        # It includes all the fields of model
        fields = '__all__'
