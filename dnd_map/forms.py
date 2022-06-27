from django import forms

from dnd_map.models import Kingdom, City, Place


class Kingdom(forms.ModelForm):
    class meta:
        # To specify the model to be used to create form
        models = Kingdom
        # It includes all the fields of model
        fields = '__all__'


class City(forms.ModelForm):
    class meta:
        # To specify the model to be used to create form
        models = City
        # It includes all the fields of model
        fields = '__all__'


class Place(forms.ModelForm):
    class meta:
        # To specify the model to be used to create form
        models = Place
        # It includes all the fields of model
        fields = '__all__'
