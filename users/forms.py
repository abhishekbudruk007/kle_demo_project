from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import CustomUsers

class CustomUserForm(UserCreationForm):
  class Meta:
      model = CustomUsers
      fields = "__all__"


class RegistrationForm(UserCreationForm):
   username = forms.CharField(widget=forms.TextInput(
       attrs={'class': 'form-control', 'placeholder': 'Username', "maxlength": "20", 'pattern': '[A-Za-z ]+',
              'title': 'Enter Characters Only ','required': 'false'}))
   email = forms.EmailField(
       widget=forms.EmailInput(
           attrs={'autofocus': 'autofocus', 'Placeholder': 'Email', 'class': "form-control",
                  'required': 'false'}))
   password1 = forms.CharField(widget=forms.PasswordInput(
       attrs={'class': 'form-control', 'placeholder': 'Password', "maxlength": "50",'required': 'false'}))
   password2 = forms.CharField(widget=forms.PasswordInput(
       attrs={'class': 'form-control', 'placeholder': 'Confirm Password', "maxlength": "50",'required': 'false'}))
   user_photo = forms.ImageField(required=False,widget=forms.ClearableFileInput(attrs={'class': 'form-control','accept': 'image/*', 'placeholder': 'User Photo'}))

   class Meta:
       model = CustomUsers
       fields = ('username','email','password1','password2','user_photo',)

