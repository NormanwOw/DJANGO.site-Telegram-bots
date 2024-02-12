from string import ascii_letters

from django import forms


class ValidateNameMixin:

    @staticmethod
    def check_name(obj, value: str):
        name = obj.cleaned_data.get(value)
        msg = {value: 'Неверный ввод.'}
        if name is None:
            return False
        for char in name:
            if char not in ascii_letters + '-':
                obj._update_errors(forms.ValidationError(msg))
                return False

        return name
