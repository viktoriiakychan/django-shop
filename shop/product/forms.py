from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from .models import DeliveryDetails


        

class ProductPlaceOrderForm(forms.Form):
    first_name = forms.CharField(label='First Name')
    last_name = forms.CharField(label='Last Name')
    email = forms.CharField(label='Email')

    address_line_1 = forms.CharField(label='Adress Line 1')
    address_line_2 = forms.CharField(label='Adress Line 2')
    country = forms.CharField(label='Country')
    city = forms.CharField(label='City')
    state = forms.CharField(label='State')
    zip_code = forms.CharField(label='ZIP Code')

    def clean(self):
        cleaned_data = super().clean()
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')
        email = cleaned_data.get('email')

        address_line_1 = cleaned_data.get('address_line_1')
        address_line_2 = cleaned_data.get('address_line_2')
        country = cleaned_data.get('country')
        city = cleaned_data.get('city')
        state = cleaned_data.get('state')
        zip_code = cleaned_data.get('zip_code')

        if not address_line_1 and not address_line_2 and not country and not city and not state and not zip_code and not first_name and not last_name and not email:
            raise forms.ValidationError('Fill in all the fields, please!')
        
class FilterByPriceForm(forms.Form):
    min_price = forms.FloatField(label='Min Price')
    max_price = forms.FloatField(label='Max Price')


    def clean(self):
        cleaned_data = super().clean()
        min_price = cleaned_data.get('min_price')
        max_price = cleaned_data.get('max_price')
        if not min_price and not max_price:
           raise forms.ValidationError('Fill in all the fields, please!')
        

class ContactForm(forms.Form):
    name=forms.CharField(label='Your name')
    email=forms.CharField(label='Email')
    subject=forms.CharField(label='Subject')
    message=forms.CharField(label='Message')


    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        email = cleaned_data.get('email')
        subject = cleaned_data.get('subject')
        message = cleaned_data.get('message')

        if not name and not email and not subject and not message:
           raise forms.ValidationError('Fill in all the fields, please!')

