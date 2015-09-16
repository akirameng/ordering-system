from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import ugettext_lazy as _
from registration.users import UserModel, UsernameField

from models import CustomUser

class RegistrationForm(UserCreationForm, forms.ModelForm):
    class Meta:
        model = UserModel()
        fields = (UsernameField(), "first_name", "last_name", "email", "phone", "image")

        help_texts = {
            'email': 'You will need to activate the account with this email.',
        }

    def clean_email(self):
        if CustomUser.objects.filter(email__iexact=self.cleaned_data['email']):
            raise forms.ValidationError(_("This email address is already in use. Please supply a different email address."))
        return self.cleaned_data['email']

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = UserModel()
        fields = (UsernameField(), "first_name", "last_name", "email", "phone", "image")
        help_texts = {
            UsernameField(): 'The username is for logging in',
            'email': 'Your email is the only prove of identification.',
        }

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True
