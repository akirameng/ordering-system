__author__ = 'lockliu'
__author__ = 'jasonZhao'

from django import forms
from django.forms import NumberInput
from models import Order, Comment_R


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ['restaurant']


class OrderDetailForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ['restaurant', 'buyer', 'delivery_type', 'paid', 'location','time', 'total_price', 'discount']



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment_R
        exclude = ['buyer', 'restaurant', 'time']
        # widgets = {
        #    'rating': NumberInput(attrs={'class' :'ratingInput'}),
        # }


class NavSearchForm(forms.Form):
  query = forms.CharField(label="",max_length=30, required=False)
  exclude=[query.label]

