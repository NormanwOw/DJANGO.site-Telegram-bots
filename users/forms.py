from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm

from users.models import User
from users.services import ValidateNameMixin


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

    def clean_email(self):
        email = self.cleaned_data.get('email')
        msg = {'email': 'Пользователь с таким Email уже существует.'}

        if email and self._meta.model.objects.filter(email=email).exists():
            self._update_errors(forms.ValidationError(msg))
        else:
            return email

    @staticmethod
    def length_msg(min_len: int, max_len: int) -> dict:
        return {
            'min_length': f'Минимальноe количество символов - {min_len}',
            'max_length': f'Максимальное количество символов - {max_len}'
        }


class ProfileForm(ValidateNameMixin, UserChangeForm):

    class Meta:
        model = User
        fields = 'first_name', 'last_name', 'email'

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.data.get('username')
        msg = {'email': 'Пользователь с таким Email уже существует.'}
        user = User.objects.filter(email=email).exclude(username=username)

        if user:
            self._update_errors(forms.ValidationError(msg))
        else:
            return email

    def clean_first_name(self):
        return self.check_name(self, 'first_name') or None

    def clean_last_name(self):
        return self.check_name(self, 'last_name') or None

