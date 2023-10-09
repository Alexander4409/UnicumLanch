from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class CustomUserCreationForm(UserCreationForm):
    phone_number = forms.CharField(max_length=15, required=True, label="Номер телефона")

    # Определите список доступных групп
    GROUP_CHOICES = (
        # ('- - класс', '- - класс'),
        ('5-6 класс', '5-6 класс'),
        ('7-8 класс', '7-8 класс'),
        ('9-11 класс', '9-11 класс'),
    )

    group = forms.ChoiceField(choices=GROUP_CHOICES, required=True, label="Возрастная группа")

    # Определите список доступных типов проектов
    Project_type_choices = (
        # ('- -', '- -'),
        ('Инженерный проект с представлением макетов или моделей','Инженерный проект с представлением макетов или моделей'),
        ('Инженерный теоретический проект','Инженерный теоретический проект'),
        ('IT проект','IT проект'),
        ('Исследовательский проект','Исследовательский проект'),
    )

    Project_type = forms.ChoiceField(choices=Project_type_choices, required=True, label="Тип проекта")

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password1', 'password2',
                  'phone_number', 'group', 'Project_type']

        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'phone_number': 'Номер телефона',
            'group': 'Возрастная группа',
            'username': 'Имя пользователя',
            'email': 'Email',
            'password1': 'Пароль',
            'password2': 'Подтвердите пароль',
            'Project_type': 'Тип проекта',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'input'})


# forms.py

from django import forms
from .models import UserFile


class UserFileForm(forms.ModelForm):
    class Meta:
        model = UserFile
        fields = ('uploaded_file',)

        labels = {
            'uploaded_file':'Загрузите файл'
        }
