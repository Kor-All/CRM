from django import forms
from django.forms.models import inlineformset_factory
from .models import Company, Address, Phone, Email
from django.utils.functional import cached_property
from django.utils.translation import ugettext as _

# class CompanyForm(forms.ModelForm):
#     class Meta:
#         model = Company
#         fields = ['name', 'director', 'description']


AddressFormSet = inlineformset_factory(Company, Address, fields=('address',))
PhoneFormSet = inlineformset_factory(Company, Phone, fields=('phone_number',))
EmailFormSet = inlineformset_factory(Company, Email, fields=('email',))




class CompanyForm(forms.ModelForm):
    name = forms.TextInput()
    director = forms.TextInput()
    description = forms.TextInput()

    class Meta:
        model = Company
        fields = ('name', 'director', 'description')

    @cached_property
    def address(self):
        return inlineformset_factory(
            Company, Address, fields=('address',))
        
            # data=self.data,
            # files=self.files,
            # instance=self.instance,
            # prefix='address',
        

    def clean(self):
        # Just in case we are subclassing some other form that does something in `clean`.
        super().clean()
        if not self.address.is_valid(self, 'address'):
            self.add_error(None, _('Please check the addresses'))

    def save(self, commit=True):
        result = super().save(commit=commit)
        self.address.save(commit=commit)
        return result


