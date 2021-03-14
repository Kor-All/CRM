from django import forms
from django.forms.models import inlineformset_factory
from .models import Company, Address, Phone, Email


AddressFormSet = inlineformset_factory(Company, Address, fields=('address',))
PhoneFormSet = inlineformset_factory(Company, Phone, fields=('phone_number',))
EmailFormSet = inlineformset_factory(Company, Email, fields=('email',))


class CompanyForm(forms.ModelForm):
  
    class Meta:
        model = Company
        fields = ('name', 'director', 'description')

