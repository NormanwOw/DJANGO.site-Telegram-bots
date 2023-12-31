from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm

from users.models import User


class LoginForm(AuthenticationForm):
    class Meta:
        model = User


class RegistrationForm(UserCreationForm):

    username = forms.CharField(
        min_length=3,
        max_length=16,
        label='Имя пользователя'
    )
    email = forms.EmailField(label='Email')
    password1 = forms.PasswordInput()
    password2 = forms.PasswordInput()

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['username'].error_messages.update(self.length_msg(3, 16))

    class Meta:
        model = User
        fields = (
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


class ProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = 'first_name', 'last_name', 'email'
