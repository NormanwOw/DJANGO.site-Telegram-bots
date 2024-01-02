from django import forms


class NewOrderForm(forms.Form):
    phone_number = forms.CharField(label='Телефон')
    bot_shop = forms.BooleanField(label='Бот-магазин', required=False)
    admin_panel = forms.BooleanField(label='Админ-панель', required=False)
    database = forms.BooleanField(label='База данных', required=False)

    class Meta:
        widgets = {
            'phone_number': forms.TextInput(attrs={'placeholder': 'Телефон'}),
        }
