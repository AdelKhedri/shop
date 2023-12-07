from django import forms
from .models import User, Profile
from django.core.exceptions import ValidationError
from mylib.validators import phone_validator, nashnal_code_validator
from django.utils.translation import gettext_lazy as _


def phone_number_exist(value):
    if User.objects.filter(phone_number=value).exists():
        raise ValidationError(_('شماره قبلا ثبت نام کرده است.'))
    

def phone_number_not_exist(value):
    if not User.objects.filter(phone_number=value).exists():
        raise ValidationError(_('شماره قبلا ثبت نام نکرده است.'))
    

def username_exist(value):
    if User.objects.filter(username=value).exists():
        raise ValidationError(_('این یوزرنیم قبلا ثبت نام کرده است.'))


def email_exist(value):
    if User.objects.filter(email=value).exists():
        raise ValidationError(_('این ایمیل قبلا ثبت نام کرده است.'))


class RegisterForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control"}), validators=[email_exist])
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}), validators=[username_exist])
    phone_number = forms.IntegerField(widget=forms.NumberInput(attrs={"class": "form-control"}), validators=[phone_validator, phone_number_exist])
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}))
    

class SininForm(forms.Form):
    phone_number = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}), validators=[phone_validator])
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    # def clean(self):
    #     cleaned_data = super().clean()
    #     phone = len(str(cleaned_data.get('phone_number')))

    #     if phone > 11 or phone < 10 :
    #         self.add_error('phone_number', ValidationError("شماره تلفن باید 11 رقم باشد"))
    #     elif len(cleaned_data.get('password')) < 5 :
    #         raise ValidationError("پسورد باید بیشتر از 4 کاراکتر باشد.")
    #     else:
    #         return cleaned_data


class ForgetPasswordForm(forms.Form):
    phone_number = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}), validators=[phone_validator, phone_number_not_exist])


class ConfirmForgetPasswordForm(ForgetPasswordForm):
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    code = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class ProfileUpdateForm(forms.ModelForm):
    nashnalcode = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}), validators=[nashnal_code_validator])
    class Meta:
        model = Profile
        fields = ['image', 'nashnalcode']
        widgets = {
            # 'nashnalcode': forms.NumberInput(attrs={'class': 'form-control'}),
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
    phone_number = forms.IntegerField(required=False ,widget=forms.NumberInput(attrs={'class': 'form-control'}), validators=[phone_validator])

    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number', "first_name", "last_name"]
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            # 'phone_number': forms.NumberInput(attrs={'class': 'form-control'}),
        }
