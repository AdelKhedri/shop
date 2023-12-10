from django import forms
from django.core.exceptions import ValidationError
from .models import Shop, Category, Product
from members.forms import phone_validator
from mylib.validators import shop_username_validator


attr = {'class':'form-control'}

class ShopAddForm(forms.Form):
    error_class = 'text-danger'
    name = forms.CharField(widget=forms.TextInput(attrs=attr))
    username = forms.CharField(widget=forms.TextInput(attrs=attr), validators=[shop_username_validator])
    description = forms.CharField(required=False, widget=forms.Textarea(attrs=attr))
    small_image = forms.ImageField(required=False, widget=forms.FileInput(attrs=attr))
    banner_image = forms.ImageField(required=False, widget=forms.FileInput(attrs=attr))
    phone_number = forms.IntegerField(required=False, widget=forms.NumberInput(attrs=attr), validators=[phone_validator])
# برای ساخت فروشگاه جدید نیاز بود منیجر فروشگاه رو با ریکویست.یوزر تایین کنم
# میتونم با تابع __init__ به ریکویست دسترسی داشته باشم
# ولی موقع استفاده از همون فرم برای ویرایش نمیتونم اینستنس بهش بدم پس دو فرم ساختم


class ShopEditeForm(forms.ModelForm):
    error_class = 'text-danger'
    phone_number = forms.IntegerField(required=False, widget=forms.NumberInput(attrs=attr), validators=[phone_validator])

    class Meta:
        model = Shop
        exclude = ['manager', 'is_active', 'coin']
        widgets = {
            'name': forms.TextInput(attrs=attr),
            'username': forms.TextInput(attrs=attr),
            'description': forms.Textarea(attrs=attr),
            'small_image': forms.FileInput(attrs=attr),
            'banner_image': forms.FileInput(attrs=attr),
            # 'phone_number': forms.NumberInput(attrs=attr),
        }


# class AddProductForm(forms.Form):
#     name = forms.CharField(max_length=150, widget=forms.TextInput(attrs=attr))
#     max_sel = forms.IntegerField(widget=forms.NumberInput(attrs=attr))
#     price = forms.IntegerField(widget=forms.NumberInput(attrs=attr))
#     category = forms.IntegerField(required=False, widget=forms.NumberInput(attrs=attr))
#     description = forms.CharField(max_length=400, required=False, widget=forms.Textarea(attrs=attr))


class UpdateProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ['shop', 'id', 'now_selled']
        widgets = {
            'name': forms.TextInput(attrs=attr),
            'max_sel': forms.NumberInput(attrs=attr),
            'proce': forms.NumberInput(attrs=attr),
            'description': forms.Textarea(attrs=attr),
            'image': forms.FileInput(attrs=attr)
        }

class CreateCategorysForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs=attr))
    for_sell = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    number_ordering = forms.IntegerField(required=False, widget=forms.NumberInput(attrs=attr))
    # products = forms.MultipleChoiceField(widget=forms.SelectMultiple(attrs=attr))


class EditeCategoryForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs=attr))
    for_sell = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class':'form-check-input'}))
    number_ordering = forms.IntegerField(widget=forms.NumberInput(attrs=attr))