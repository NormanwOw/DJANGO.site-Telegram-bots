from django.db import models
from django.contrib.auth.models import AbstractUser


class UserModel(AbstractUser):

    first_name = models.CharField(
        max_length=20, verbose_name='Имя', blank=True, null=True
    )
    last_name = models.CharField(
        max_length=20, verbose_name='Фамилия', blank=True, null=True
    )

    class Meta:
        db_table = 'user'
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    def __str__(self):
        return self.username
