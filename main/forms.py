from django import forms
from main.models import Order


class NewOrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ['email', 'phone_number', 'admin_panel', 'database']
        widgets = {
            'phone_number': forms.TextInput(attrs={'placeholder': 'Телефон'}),
            'email': forms.TextInput(attrs={'placeholder': 'Email'}),
        }
