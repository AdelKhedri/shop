from django import forms
from django.core.exceptions import ValidationError
from .models import Shop


attr = {'class':'form-control'}

class ShopAddForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs=attr))
    username = forms.CharField(widget=forms.TextInput(attrs=attr))
    description = forms.CharField(required=False, widget=forms.Textarea(attrs=attr))
    small_image = forms.ImageField(required=False, widget=forms.FileInput(attrs=attr))
    banner_image = forms.ImageField(required=False, widget=forms.FileInput(attrs=attr))
    phone_number = forms.IntegerField(required=False, widget=forms.NumberInput(attrs=attr))
# برای ساخت فروشگاه جدید نیاز بود منیجر فروشگاه رو با ریکویست.یوزر تایین کنم
# میتونم با تابع __init__ به ریکویست دسترسی داشته باشم
# ولی موقع استفاده از همون فرم برای ویرایش نمیتونم اینستنس بهش بدم پس دو فرم ساختم

class ShopEditeForm(forms.ModelForm):

    class Meta:
        model = Shop
        exclude = ['manager', 'is_active', ]
        widgets = {
            'name': forms.TextInput(attrs=attr),
            'username': forms.TextInput(attrs=attr),
            'description': forms.Textarea(attrs=attr),
            'small_image': forms.FileInput(attrs=attr),
            'banner_image': forms.FileInput(attrs=attr),
            'phone_number': forms.NumberInput(attrs=attr),
        }