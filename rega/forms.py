from django.db import models
from .models import User, PropertyObject
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


class PropertyObjectForm(forms.ModelForm):

    class Meta:
        model = PropertyObject
        fields = ['latitude', 'longitude', 'square', 'price', 'type', 'address', 'sold_status']
        widgets = {
            'latitude': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. 124.564577',
                'type': 'text'
            }),
            'longitude': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. 124.564577',
                'type': 'text'
            }),
            'square': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'square of object',
                'type': 'text'
            }),
            'price': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'price of object',
                'type': 'text'
            }),
            'type': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. apartment',
                'type': 'text'
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'address of the building',
                'type': 'text'
            }),
            'sold_status': forms.TextInput(attrs={
                'class': 'form-check-input',
                'type': 'checkbox',
                'name': 'sold_status',
                'id': ['sold_status']
            })
        }

    def clean(self):
        latitude = self.cleaned_data['latitude']
        longitude = self.cleaned_data['longitude']
        square = self.cleaned_data['square']
        price = self.cleaned_data['price']
        type = self.cleaned_data['type']
        address = self.cleaned_data['address']
        if latitude and longitude and square and price and type and address:
            return self.cleaned_data
        else:
            raise forms.ValidationError(f'The fields were entered incorrect!')



        # <input class="form-check-input" type="radio" name="gridRadios" id="gridRadios1" value="option1" checked>
        #         <label class="form-check-label" for="gridRadios1">
        #             Администратор
        #         </label>
