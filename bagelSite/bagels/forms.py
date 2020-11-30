from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, help_text='Required.')
    last_name = forms.CharField(max_length=30, help_text='Required.')
    email = forms.EmailField(max_length=254, help_text='Required. Must be a valid email address.')
    phone_number = forms.CharField(max_length=15, help_text='Required. Format: XXXXXXXXXXXXXXX')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'phone_number', 'password1', 'password2', )


class EditProfileForm(UserChangeForm):
    password = None
    phone_number = forms.CharField(max_length=15, help_text='Required. Format: XXXXXXXXXXXXXXX')

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone_number',)
