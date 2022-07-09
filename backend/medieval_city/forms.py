from django import forms
from django.contrib.auth.models import User
from .models import Civilian


class LoginForm(forms.Form):
    username = forms.CharField(label='Имя пользователя')
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')

    def clean_password2(self):
        clean_data = self.cleaned_data
        if clean_data['password'] != clean_data['password2']:
            raise forms.ValidationError('Пароли не совпадают!')
        return clean_data['password2']


# TODO optimize me, plz
class CivilianForm(forms.ModelForm):
    class Meta:
        model = Civilian
        fields = '__all__'  # TODO newer do things like this
