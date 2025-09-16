from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from myauth.models import RegistrationCode

class UserCreationForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Jane'})
    )
    last_name = forms.CharField(
        required=True,
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Doe'})
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'jane@doe.com'})
    )
    username = forms.CharField(
        required=True,
        max_length=25,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'jane.doe'})
    )
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirm Password'})
    

    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data['email']).exists():
            raise forms.ValidationError("Email already exists.")
        return self.cleaned_data['email']

    def clean_username(self):
        if User.objects.filter(username=self.cleaned_data['username']).exists():
            raise forms.ValidationError("Username already exists.")
        return self.cleaned_data['username']

    def save(self, commit=True):        
        user = super().save(commit=False)
        user.is_active = False
        if commit:
            user.save()
        return user

class ConfirmRegistrationForm(forms.Form):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'jane@doe.com'})
    )
    confirmation_code = forms.CharField(
        required=True,
        max_length=6,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '123456'})
    )
    class Meta:
        model = RegistrationCode
        fields = ('code', 'email')

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=25,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )

class ResetPasswordForm(forms.Form):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'jane@doe.com'})
    )

class ConfirmPasswordResetForm(forms.Form):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'jane@doe.com'})
    )
    reset_code = forms.CharField(
        required=True,
        max_length=6,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '123456'})
    )
    new_password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'New Password'})
    )
    repeat_password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Repeat New Password'})
    )

class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Old Password'})
    )
    new_password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'New Password'})
    )
    repeat_password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Repeat New Password'})
    )