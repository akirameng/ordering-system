__author__ = 'JC'

from django import forms
from models import Restaurant, Address, Dish


class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        exclude = ['baseUser', ]
        help_texts = {
            'name': 'Everybody can see your restaurant name.',
            'phone': 'Giving out your business phone number is not mandatory, but it is very important to customers.'
        }

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        exclude = ['restaurant', 'latitude', 'longitude']


class DishForm(forms.ModelForm):
    class Meta:
        model = Dish
        exclude = ['restaurant', 'status', 'liked', 'unliked']

