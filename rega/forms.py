from django.db import models
from .models import User
# from django.forms import ModelForm, TextInput, fields, widgets, RadioSelect
from django import forms

class LoginForm(forms.ModelForm):
    # email = forms.CharField(widget=forms.TextInput)
    # password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email', 'password']
        widgets = {
            'email': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите эл.почту',
                'type': 'text'
            }),
            'password': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите пароль',
                'type': 'password'
            })
        }

    def clean(self):
        email =  self.cleaned_data['email']
        password =  self.cleaned_data['password']

        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError(u'Пользователь с емейлом {email} не найден в системе.')
        user = User.objects.filter(email=email).first()
        if user:
            if not user.check_password(password):
                raise forms.ValidationError(u'Пароль или логин не вырные!')

        return self.cleaned_data




class RegistrationForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password', 'type']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите имя',
                'type': 'text'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите фамилию',
                'type': 'text'
            }),
            'email': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите эл.почту',
                'type': 'email'
            }),
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите ник',
                'type': 'text'
            }),
            'password': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите пароль',
                'type': 'password'
            }),
            'type': forms.TextInput(attrs={
                'class': 'form-check-input',
                'type': 'radio',
                'name': 'gridRadios',
                'id': ['gridRadios1', 'gridRadios2', 'gridRadios3'],
                'value': ['admin', 'manager', 'chair'],
            })
        }

    def clean_email(self):
        email = self.cleaned_data['email']

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(f'Пользователь с таким емейлом уже зарегистрирован!')

        return email
        

    def clean_username(self):
        username = self.cleaned_data['username']

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(f'Этот никнейм занят!')

        return username

    def clean(self):
        return self.cleaned_data



        # <input class="form-check-input" type="radio" name="gridRadios" id="gridRadios1" value="option1" checked>
        #         <label class="form-check-label" for="gridRadios1">
        #             Администратор
        #         </label>
