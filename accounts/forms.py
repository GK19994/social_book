from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser,UploadedFile

class SignUpForm(UserCreationForm):

    password2 = forms.CharField(label = "Confirm Password", widget=forms.PasswordInput)

    class Meta:
        model =CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'birth_year', 'address', 'public_visibility']
        labels = {'email': 'Email'}



class UploadFileForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ['file', 'title', 'description', 'visibility', 'cost', 'year_published']
        widgets = {
            'file': forms.ClearableFileInput(attrs={'accept': 'application/pdf,image/jpeg/'}),
        }

# class UserRegistrationForm(forms.ModelForm):
#     password = forms.CharField(label='Password', widget=forms.PasswordInput)
#     password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)
    
#     class Meta:
#         model = User
#         fields = ('username', 'first_name', 'last_name', 'email')
    
#     def clean_password2(self):
#         cd = self.cleaned_data
#         if cd['password'] != cd['password2']:
#             raise forms.ValidationError('Passwords don\'t match.')
#         return cd['password2']

