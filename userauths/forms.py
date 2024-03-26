from django import forms
from django.contrib.auth.forms import UserCreationForm
from userauths.models import User
class UserRegisterForm(UserCreationForm):
    username = forms.CharField( widget=forms.TextInput(attrs={"placeholder": "Username", "class": "form-control bg-transparent" , "name" : "Username"}))
    email = forms.EmailField( widget=forms.TextInput(attrs={"placeholder": "Email", "class": "form-control bg-transparent" , "name" : "Email"}))
    password1 = forms.CharField( widget=forms.PasswordInput(attrs={"placeholder": "Password", "class": "form-control bg-transparent" , "name" : "password"}))
    password2 = forms.CharField( widget=forms.PasswordInput(attrs={"placeholder": "Repeat Password", "class": "form-control bg-transparent" , "name" : "RepeatPassword"}))

    class Meta:
        model = User
        fields = ['username','email']