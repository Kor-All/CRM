from django import forms
from django.contrib.auth.models import User

from .models import Profile


class UserUpdateForm(forms.ModelForm):
    """A class used to update the form for User

    Attributes (Meta):
        email : form field
        model (class): Database's table
        fields (list): List of fields.
    """  
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class ProfileUpdateForm(forms.ModelForm):
    """A class used to update the form for Users profile

    Attributes (Meta):
        model (class): Database's table
        fields (list): List of fields.
    """  
    class Meta:
        model = Profile
        fields = ['image']