from django.forms import ModelForm
from .models import *
from django import forms

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields= '__all__'
        exclude=['user','food_list']
    # Optional: if you need to validate or handle the clearing of the image manually:
    def clean_logo_image(self):
        logo_image_clear = self.cleaned_data.get('logo_image-clear', False)
        if logo_image_clear:
            return None  # Return None to clear the image
        return self.cleaned_data.get('logo_image')
class FoodForm(forms.ModelForm):
    clear_image_url = forms.BooleanField(required=False)
    pre_food_image=forms.CharField(max_length=255, required=False, label='pre_food_image')
    new_category = forms.CharField(max_length=255, required=False, label='New Category')

    class Meta:
        model = Food
        fields = ['index', 'pre_food_image','food_title', 'food_price', 'category', 'description', 'food_image', 'clear_image_url']
        widgets = {
            'index': forms.HiddenInput(),
            'pre_food_image':forms.HiddenInput()
        }

 
# class FoodForm(forms.ModelForm):
#     clear_image_url = forms.BooleanField(required=False)
#     category = forms.CharField(
#         widget=forms.TextInput(attrs={'list': 'food_categories'}),
#         label='Food Category',
#         required=False
#     )

#     def __init__(self, *args, **kwargs):
#         categories = kwargs.pop('categories', None)
#         super().__init__(*args, **kwargs)

#         if categories:
#             # Populate the <datalist> with unique food categories
#             self.fields['category'].widget.attrs['list'] = 'food_categories'
#             self.fields['category'].widget.choices = [(category, category) for category in categories]

#     class Meta:
#         model = Food
#         fields = ['index', 'food_title', 'food_price', 'category', 'description', 'food_image', 'clear_image_url']
#         widgets = {
#             'index': forms.HiddenInput()
#         }