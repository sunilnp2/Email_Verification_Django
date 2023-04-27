from django import forms
from django.contrib.auth.forms import  AuthenticationForm
from django.contrib.auth import get_user_model
from myapp.models import User



class UserRegistrationForm(forms.ModelForm):
    email = forms.EmailField(help_text='A valid email address, please.')
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    # password2 = forms.CharField(widget={forms.PasswordInput})
    class Meta:
        model = User
        fields = ['username','email', 'name', 'password']

    # def save(self, commit=True):
    #     user = super(UserRegistrationForm, self).save(commit=False)
    #     user.email = self.cleaned_data['email']
    #     if commit:
    #         user.save()

    #     return user

class UserLoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'password']
# class UserUpdateForm(forms.ModelForm):
#     email = forms.EmailField()

#     class Meta:
#         model = get_user_model()
#         fields = ['first_name', 'last_name', 'email', 'image', 'description']