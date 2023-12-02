from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
# from members.views import User


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