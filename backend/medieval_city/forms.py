from django import forms
from django.contrib.auth.models import User
from .models import Civilian, City, Estate


class LoginForm(forms.Form):
    username = forms.CharField(label='Имя пользователя')
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')

    def clean_second_password(self):
        clean_data = self.cleaned_data
        if clean_data['password'] != clean_data['password2']:
            raise forms.ValidationError('Пароли не совпадают!')
        return clean_data['password2']


class CivilianForm(forms.ModelForm):

    class Meta:
        model = Civilian
        fields = ['name',
                  'surname',
                  'age',
                  'estate',
                  'senior',
                  'income',
                  'city',
                  'vassals']

    vassals = forms.ModelMultipleChoiceField(
        queryset=Civilian.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        label='Вассалы'
    )

    city = forms.ModelMultipleChoiceField(
        queryset=City.objects.all(),
        widget=forms.Select,
        label='Город'
    )

    def clean(self):
        clean_data = self.cleaned_data
        current_civilian_estate_id = Estate.objects.get(class_name=clean_data['estate']).id
        vassals = clean_data.get('vassals')
        if vassals:
            vassals_estates_ids = [vassal.estate.id for vassal in vassals]
            if any([current_civilian_estate_id > vassal_id for vassal_id in vassals_estates_ids]):
                raise forms.ValidationError('Сословие вассала не может быть старше сословия сеньора')
            else:
                return self.cleaned_data
