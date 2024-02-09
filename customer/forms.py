from django import forms
from django.forms import ModelForm
from django.shortcuts import get_object_or_404
# from django.core.exceptions import ValidationError
# from django.contrib.auth.forms import  AuthenticationForm

from . import models



def clean_contact_no(phone):
    try:
        max_length, min_length = 15, 10
        ph_length = len(str(phone))
        if not (min_length <= ph_length <= max_length):
            raise forms.ValidationError('Contact number length is not valid!')
    except (ValueError, TypeError) as exc:
        raise forms.ValidationError("Please enter a valid contact number!") from exc

    return phone


   
       
class CustomerRegistrationForm(ModelForm):
    phone = phone = forms.CharField(validators=[clean_contact_no], widget=forms.TextInput(attrs={'required': 'required', 'type': 'tel'}))

    class Meta:
        model = models.Customer
        widgets={
            "first_name": forms.TextInput(attrs={'required': "required"}),
            "last_name": forms.TextInput(attrs={'required': "required"}),
            "birth_date": forms.NumberInput(attrs={'required': "required"}),
            "street": forms.TextInput(attrs={'required': "required"}),
            "city": forms.TextInput(attrs={'required': "required"}),
            "state": forms.TextInput(attrs={'required': "required"}),
            "country": forms.TextInput(attrs={'required': "required"}),
            "pin_code": forms.NumberInput(attrs={'required': "required"}),
            "balance":forms.NumberInput(attrs={'required': "required"}),
        }
        fields=['first_name','last_name', 'birth_date', 'phone_number','street','city','state','country','pin_code','balance']



class WithdrawForm(forms.Form):
    amount = forms.DecimalField(
        label='Withdrawal Amount',
        max_digits=10,
        decimal_places=2,
        min_value=0.01,
        widget=forms.NumberInput(attrs={'step': '0.01'})
    )

class TransferForm(forms.Form):
    amount = forms.DecimalField(
        label='Transfer Amount',
        max_digits=10,
        decimal_places=2,
        min_value=0.01,
        widget=forms.NumberInput(attrs={'step': '0.01'})
    )
    recipient_account_number = forms.CharField(
        label='Recipient Account Number',
        max_length=200,
        widget=forms.TextInput(attrs={'placeholder': 'Enter recipient account number'})
    )
    transfer_purpose = forms.CharField(
        label='Transfer Purpose',
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Optional: Enter transfer purpose'})
    )
    transfer_date = forms.DateField(
        label='Transfer Date',
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    description = forms.CharField(
        label='Description',
        max_length=500,
        required=False,
        widget=forms.Textarea(attrs={'placeholder': 'Optional: Enter transfer description'})
    )

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount <= 0:
            raise forms.ValidationError('Amount must be greater than zero.')
        return amount

    def clean_recipient_account_number(self):
        recipient_account_number = self.cleaned_data.get('recipient_account_number')

        if not recipient_account_number:
            raise forms.ValidationError('Recipient account number is required.')

        try:
            recipient_customer = get_object_or_404(models.Customer, account_no=recipient_account_number)
        except:
            raise forms.ValidationError('Recipient account number does not exist.')

        return recipient_account_number





