from collections.abc import Mapping
from typing import Any
from django import forms
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
from .models import User, Profile
from django.core.exceptions import ValidationError

class RegisterForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control"}))
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    phone_number = forms.IntegerField(widget=forms.NumberInput(attrs={"class": "form-control"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}))

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 != password2:
            raise ValidationError('پسورد ها نباید متفاوت باشند.')
        elif User.objects.filter(username=cleaned_data.get('username')).exists():
            raise ValidationError("این یوزرنیم قبلا در سایت ثبت نام کرده است.")
        elif User.objects.filter(phone_number=int(cleaned_data.get('phone_number'))).exists():
            raise ValidationError("شماره تلفن قبلا در سایت ثبت نام کرده است.")
        elif User.objects.filter(email=cleaned_data.get("email")).exists():
            raise ValidationError("این ایمیل قبلا ثبت نام کرده است.")
        else:
            return cleaned_data

class SininForm(forms.Form):
    phone_number = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean(self):
        cleaned_data = super().clean()
        phone = len(str(cleaned_data.get('phone_number')))

        if phone > 11 or phone < 10 :
            self.add_error('phone_number', ValidationError("شماره تلفن باید 11 رقم باشد"))
        elif len(cleaned_data.get('password')) < 5 :
            raise ValidationError("پسورد باید بیشتر از 4 کاراکتر باشد.")
        else:
            return cleaned_data


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean(self):
        clean_data = super().clean()
        new_password1 = clean_data.get("new_password1")
        new_password2 = clean_data.get("new_password2")

        if new_password1 != new_password2:
            raise ValidationError("پسورد ها نباید متفاوت باشند.")
        else:
            return clean_data


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'nashnalcode']
        widgets = {
            'nashnalcode': forms.NumberInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': ''})
        }
    
    def clean(self):
        cleaned_data = super().clean()
        nashnalcode = len(str(cleaned_data.get('nashnalcode')))
        
        if nashnalcode != 10:
            raise ValidationError("کد ملی باید ۱۰ رقم باشد.")
        else:
            return cleaned_data

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=False ,widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(required=False ,widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(required=False ,widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number', "first_name", "last_name"]
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.NumberInput(attrs={'class': 'form-control'}),
        }
