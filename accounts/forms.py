from django import forms
from .models import User


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'password'}), min_length=8)
    conform_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'conform password'}), min_length=8)

    class Meta:
        model = User

        fields = ['first_name', 'last_name', 'username', 'email', 'password']




    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get('password')
        conform_password = cleaned_data.get('conform_password')
        if password != conform_password:
            raise forms.ValidationError("password didn't match. ")

