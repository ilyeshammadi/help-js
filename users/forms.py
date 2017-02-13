from django import forms

from .models import User


class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')
        widgets = {
            'password': forms.TextInput(attrs={'type': 'password'}),
        }


class RegisterForm(forms.ModelForm):
    confirmed_password = forms.CharField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'confirmed_password')
        widgets = {
            'password': forms.TextInput(attrs={'type': 'password'}),
            'confirmed_password': forms.TextInput(attrs={'type': 'password'}),
        }
