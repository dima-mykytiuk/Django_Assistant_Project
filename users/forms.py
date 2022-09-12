from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django import forms
from django.core.exceptions import ValidationError

from users.utils import send_email_for_verify


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, widget=forms.TextInput)
    password = forms.CharField(max_length=100, widget=forms.PasswordInput)
    