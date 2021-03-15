from django import forms
from django.forms.models import inlineformset_factory
from .models import Company, Address, Phone, Email


AddressFormSet = inlineformset_factory(Company, Address, form=forms.ModelForm, fields=('address',), extra=2)
PhoneFormSet = inlineformset_factory(Company, Phone, form=forms.ModelForm, fields=('phone_number',), extra=2)
EmailFormSet = inlineformset_factory(Company, Email, form=forms.ModelForm, fields=('email',), extra=2)


class CompanyForm(forms.ModelForm):
    """A class used to create the form for companies

    Attributes (Meta):
        model (class): Database's table
        fields (list): List of fields.
    """  
    class Meta:
        model = Company
        fields = ('name', 'director', 'description')

