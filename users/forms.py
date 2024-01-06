from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from users.models import User


class LoginForm(AuthenticationForm):
    class Meta:
        model = User


class RegistrationForm(UserCreationForm):

    first_name = forms.CharField(
        min_length=2,
        max_length=20,
    )
    last_name = forms.CharField(
        min_length=2,
        max_length=20,
    )
    username = forms.CharField(
        min_length=3,
        max_length=16,
    )
    email = forms.EmailField()
    password1 = forms.PasswordInput()
    password2 = forms.PasswordInput()

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)

        self.fields['first_name'].error_messages.update(self.length_msg(2, 20))
        self.fields['last_name'].error_messages.update(self.length_msg(2, 20))
        self.fields['username'].error_messages.update(self.length_msg(3, 16))

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

    @staticmethod
    def length_msg(min_len, max_len: str) -> dict:
        return {
            'min_length': f'Минимальноe количество символов - {min_len}',
            'max_length': f'Максимальное количество символов - {max_len}'
        }
