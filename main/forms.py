from django import forms

from phonenumber_field.formfields import PhoneNumberField


class NewOrderForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(NewOrderForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name == 'phone_number' and 'invalid' in field.error_messages:
                field.error_messages['invalid'] = 'Введите корректный номер телефона'

    phone_number = PhoneNumberField(label='Телефон', region='RU')
    bot_shop = forms.BooleanField(label='Бот-магазин', required=False)
    admin_panel = forms.BooleanField(label='Админ-панель', required=False)
    database = forms.BooleanField(label='База данных', required=False)
