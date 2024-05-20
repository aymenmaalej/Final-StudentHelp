from django import forms
from .models import TransportPost, CustomUser
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model,authenticate
User = get_user_model()



class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'name', 'surname', 'phone_number', 'id_number', 'photo', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fieldname in ['email', 'name', 'surname', 'phone_number', 'id_number', 'photo']:
            self.fields[fieldname].required = True

class LoginForm(AuthenticationForm):
    email = forms.EmailField(label='Email')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

class OfferForm(forms.ModelForm):
    class Meta:
        model = TransportPost
        fields = ['departure', 'destination', 'departure_time', 'seats_available', 'contact_info']
        labels = {
            'departure': 'Departure',
            'destination': 'Destination',
            'departure_time': 'Departure Time',
            'seats_available': 'Seats Available',
            'contact_info': 'Contact Information',
        }
        widgets = {
            'departure_time': forms.TextInput(attrs={'placeholder': 'HH:MM AM/PM'}),
        }

class TransportPostForm(forms.ModelForm):
    class Meta:
        model = TransportPost
        exclude = ['user']