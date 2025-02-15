from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, Report, Category, Problem

class CustomUserCreationForm(UserCreationForm):
    full_name = forms.CharField(
        label='ФИО',
        max_length=255,
        required=True
    )
    email = forms.EmailField(
        label='Email',
        required=True
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'full_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Логин'
        self.fields['password1'].label = 'Пароль'
        self.fields['password2'].label = 'Подтверждение пароля'

    def save(self, commit=True):
        user = super().save(commit=False)
        user.full_name = self.cleaned_data['full_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['title', 'description', 'category', 'image']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите название'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Введите описание',
                'rows': 3
            }),
            'category': forms.Select(attrs={
                'class': 'form-control'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            })
        }

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            if image.size > 10 * 1024 * 1024:  # 10MB в байтах
                raise forms.ValidationError("Размер файла не должен превышать 10МБ")
        return image

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название категории'})
        }

class CategoryCreateForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите название категории'})
        }

class ProblemUpdateForm(forms.ModelForm):
    class Meta:
        model = Problem
        fields = ['status', 'rejection_reason', 'image_after']