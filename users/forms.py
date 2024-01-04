from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import AbstractUser


class LoginForm(AuthenticationForm):
    class Meta:
        model = AbstractUser
