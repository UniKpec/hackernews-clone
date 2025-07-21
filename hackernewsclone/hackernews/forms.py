from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .models import SubmitStory

class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["username","password"]

class LoginForm(AuthenticationForm):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class Usersubmit(forms.ModelForm):
    class Meta:
        model = SubmitStory
        fields = ["title","url","text"]

        widgets = {
            "title" : forms.TextInput(attrs={"size":52}),
            "url": forms.URLInput(attrs={"size":52}),
            "text": forms.Textarea(attrs={"rows":5, "cols":50,}),
        }
    