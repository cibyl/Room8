'''
app.forms.py

Arquivo responsável por gerenciar lvalidação de FORMS dentro da
aplicação 'app'.
'''

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import User

User = get_user_model()

# Classe de cadastro
class RegisterForm(forms.Form):
	email     = forms.CharField(required=True)
	nome      = forms.CharField(required=True)
	telefone  = forms.CharField(required=True)
	password1 = forms.CharField(required=True)
	password2 = forms.CharField(required=True)
	
