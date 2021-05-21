from django.db import models
from .models import User
from django.forms import ModelForm, TextInput, fields, widgets, RadioSelect

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['name', 'email', 'password', 'type']
        widgets = {
            'name': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите имя',
                'type': 'text'
            }),
            'email': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите эл.почту',
                'type': 'email'
            }),
            'password': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите пароль',
                'type': 'password'
            }),
            'type': TextInput(attrs={
                'class': 'form-check-input',
                'type': 'radio',
                'name': 'gridRadios',
                'id': ['gridRadios1', 'gridRadios2', 'gridRadios3'],
                'value': ['option1', 'option2', 'option3'],
            })
        }



        # <input class="form-check-input" type="radio" name="gridRadios" id="gridRadios1" value="option1" checked>
        #         <label class="form-check-label" for="gridRadios1">
        #             Администратор
        #         </label>