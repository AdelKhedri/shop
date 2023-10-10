from django import forms
from django.core.exceptions import ValidationError
from .models import Card, Transaction

class CardForm(forms.Form):
    shaba_number = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    card_number = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control'}))

    
    def clean(self, *args, **kwargs):
        cleaned_data = super().clean(*args, **kwargs)
        card_number = str(cleaned_data.get('card_number'))
        shaba_number = str(cleaned_data.get('shaba_number'))
        print(f"len-{len(card_number)}/ {card_number}")
        print(f"len-{len(shaba_number)}/ {shaba_number}")
        if len(card_number) != 16:
            raise ValidationError('شماره کارت باید 16 رقم باشد.')
        elif len(shaba_number) != 24:
            raise ValidationError('شماره شبا باید  24 رقم باشد.')
        else:
            return cleaned_data


class TransactionForm(forms.Form):
    transaction_type_list = (('withdraw', 'برداشت'), ('deposit', 'پرداخت'))
    transaction_type = forms.ChoiceField(choices=transaction_type_list, widget=forms.Select(attrs={'class': 'form-control'}))
    description =  forms.CharField(required=False ,widget=forms.Textarea(attrs={'class': 'form-control'}))
    amount =  forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))