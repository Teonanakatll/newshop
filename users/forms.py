from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from users.models import User


class UserLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']
    # username = forms.CharField()
    # password = forms.CharField()
    # username = forms.CharField(
    #     label='имя',
    #     widget=forms.TextInput(attrs={'autofocus': True,
    #                                   'class': 'form-control',
    #                                   'placeholder': 'Введите имя пользователя'
    #                                   }))
    # password = forms.CharField(
    #     label='пароль',
    #     widget=forms.PasswordInput(attrs={'autocomplete': 'current-password',
    #                                       'class': 'form-control',
    #                                       'placeholder': 'Введите пароль'
    #                                       }))

class UserRegistrationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

        first_name = forms.CharField()
        last_name = forms.CharField()
        username = forms.CharField()
        email = forms.CharField()
        password1 = forms.CharField()
        password2 = forms.CharField()
        
    # first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
    #                                                            'plaseholder': 'Введите ваше имя'}))
    #
    # last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
    #                                                            'plaseholder': 'Введите вашу фамилию'}))
    #
    # username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
    #                                                            'plaseholder': 'Введите имя пользователя'}))
    #
    # email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control',
    #                                                            'plaseholder': 'Введите ваш email'}))
    #
    # password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control',
    #                                                            'plaseholder': 'Введите ваш пароль'}))
    #
    # password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control',
    #                                                            'plaseholder': 'Подтвердите ваш пароль'}))