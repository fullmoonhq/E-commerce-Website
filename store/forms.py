from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm,PasswordResetForm
from .models import User
from django import forms

class UserForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control my-3','placeholder':'Username'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control my-3','placeholder':'Email'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control my-3','placeholder':'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control my-3','placeholder':'Confirm Password'}))
    class Meta:
        model = User
        fields = ['username','email','password1','password2']

class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete':'current-password','class':'form-control my-3','placeholder':'Old Password'}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete':'current-password','class':'form-control my-3','placeholder':'New Password'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete':'current-password','class':'form-control my-3','placeholder':'Confirm New Password'}))

class ResetPasswordForm(PasswordResetForm):
    email = forms.EmailField(widget = forms.EmailInput(attrs={'class':'form-control','placeholder':'Email Id'}))