from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from users.models import User


class LoginForm(AuthenticationForm):
    class Meta:
        model = User


class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(min_length=2, max_length=20)
    last_name = forms.CharField(min_length=2, max_length=20)
    username = forms.CharField(min_length=3, max_length=16)
    email = forms.EmailField()
    password1 = forms.PasswordInput()
    password2 = forms.PasswordInput()

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'username',
            'email',
            'password1',
            'password2',
        )
