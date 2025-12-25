from django import forms
from .models import Tweet, Team, Driver
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class TweetForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = ['text', 'photo', 'post_type', 'team', 'driver']
        widgets = {
            'text': forms. Textarea(
                attrs={
                    'rows': 3,
                    'placeholder': "Share your F1 thoughts..."
                }
            ),
        }


class PollOptionForm(forms.Form):
    option_1 = forms.CharField(max_length=100, required=False, label="Option 1")
    option_2 = forms.CharField(max_length=100, required=False, label="Option 2")
    option_3 = forms.CharField(max_length=100, required=False, label="Option 3")
    option_4 = forms.CharField(max_length=100, required=False, label="Option 4")


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")