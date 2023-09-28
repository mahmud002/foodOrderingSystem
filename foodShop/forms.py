from django.forms import ModelForm
from .models import *
from django import forms

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields= '__all__'
        exclude=['user','food_list']
class FoodForm(forms.ModelForm):
    clear_image_url = forms.BooleanField(required=False)
    class Meta:
        model = Food
        fields=  ['index', 'food_title','food_price','category','description','food_image', 'clear_image_url']
        widgets = {
            'index': forms.HiddenInput()
        }
