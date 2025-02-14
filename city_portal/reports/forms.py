from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, Report

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'full_name', 'email', 'password1', 'password2']

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['title', 'description', 'category', 'image']
