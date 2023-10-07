from django import forms
from .models import User

class RegisterForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={}))

    class Meta:
        model = User
        fields = "__all__"
        