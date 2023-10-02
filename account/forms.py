from django import forms
from django.contrib.auth.models import User

from .models import Profile


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Пароль',
                               widget=forms.PasswordInput)
    password2 = forms.CharField(label='Подтверждение пароля',
                                widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Password don\'t match.')
        return cd['password2']


class UserEditForm(UserRegistrationForm):
    email = forms.EmailField(label='E-mail',
                             widget=forms.EmailInput)
    class Meta:
        model = User
        fields = ['email', 'password']


class ProfileEditForm(forms.ModelForm):
    photo = forms.ImageField(widget=forms.FileInput)

    class Meta:
        model = Profile
        fields = ['photo']
