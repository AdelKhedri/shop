from django import forms
from django.core.exceptions import ValidationError
from .models import Card, Transaction
from mylib.validators import card_number_validator, shaba_number_validator

class CardForm(forms.Form):
    shaba_number = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}), validators=[shaba_number_validator])
    card_number = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control'}), validators=[card_number_validator])


class TransactionForm(forms.Form):
    transaction_type_list = (('withdraw', 'برداشت'), ('deposit', 'پرداخت'))
    transaction_type = forms.ChoiceField(choices=transaction_type_list, widget=forms.Select(attrs={'class': 'form-control'}))
    description =  forms.CharField(required=False ,widget=forms.Textarea(attrs={'class': 'form-control'}))
    amount =  forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))