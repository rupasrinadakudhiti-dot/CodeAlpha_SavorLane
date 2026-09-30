from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Order


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=60)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email', 'password1', 'password2')


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('full_name', 'email', 'phone', 'fulfillment', 'preferred_window', 'address', 'city', 'pincode', 'notes')
        widgets = {
            'address': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Street and house number (delivery only)'}),
            'notes': forms.TextInput(attrs={'placeholder': 'Optional instructions'}),
        }

    def clean(self):
        data = super().clean()
        if data.get('fulfillment') == 'DELIVERY':
            for name in ('address', 'city', 'pincode'):
                if not data.get(name):
                    self.add_error(name, 'Required for delivery.')
        return data
