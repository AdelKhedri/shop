from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from ShopApp.models import Shop


def phone_validator(value):
    value = str(value)
    if len(value) > 11:
        raise ValidationError(_("شماره تلفن نباید بیشتر از 11 رقم باشد"))
    elif len(value) < 10:
        raise ValidationError(_("شماره تلفن نباید کوچک تر از ۱۰ رقم باشد"))
    elif len(value) == 10 and value[0] != '9':
        raise ValidationError(_("شماره تلفن باید با 0 یا9 شروع شود"))
    elif len(value) == 11 and value[0:2] != '09':
        raise ValidationError(_("شماره تلفن نادرست است."))


def nashnal_code_validator(value):
    if len(str(value)) != 10:
        raise ValidationError(_('کد ملی باید ۱۰ رقم باشد.'))


def shop_username_validator(value):
    if Shop.objects.filter(username=value).exists():
        raise ValidationError(_('فروشگاهی با این نام از قبل وجود دارد'))


def card_number_validator(value):
    if value.isalpha():
        raise ValidationError(_('شماره کارت نباید حاوی کاراکتر غیر عددی باشد.'))
    elif value[0] == '0':
        raise ValidationError(_('شماره کارت نباید با 0 شروع شود'))
    elif len(value) != 16 :
        raise ValidationError(_('شماره کارت باید ۱۶ رقم باشد'))


def shaba_number_validator(value):
    value = str(value)
    if value.isalpha():
        raise ValidationError(_('شماره شبا نباید حاوی کارکتر غیر عددی باشد.'))
    elif len(value) != 24:
        raise ValidationError(_('شماره شبا باید 24 رقم باشد.'))


