'''
app.views.py

Arquivo responsável por gerenciar lógicas de chamadas VMC dentro da
aplicação 'app'.
'''

import os, tempfile
from django.conf import settings
from django.core.urlresolvers import reverse
from django.views import generic
from django.views.decorators.http import require_POST
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.db import IntegrityError
from django.db.models import F, FloatField, Sum
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template.loader import get_template
from django.template import RequestContext
from django.forms.models import model_to_dict
import json
from .forms import forms, RegisterForm
from .models import Imoveis, Mensagens
from datetime import datetime, date
from decimal import Decimal
import random

# Seta objeto User principal

User = get_user_model()


## Funcoes de log

# Print padrão de erro
def print_erro(msg):
	print('\033[0;31m-+- ((ERRO)) -+-\033[0m -*- {0} -*-'.format(msg))

# Print padrão de respostas REST
def print_rest(msg):
	print('\033[0;34m-+- ((REST)) -+-\033[0m -*- {0} -*-'.format(msg))

# Print padrão de sucesso
def print_ok(msg):
	print('\033[0;32m-+- ((OK)) -+-\033[0m -*- {0} -*-'.format(msg))


# View principal
def index(request):

	imoveis = Imoveis.objects.order_by('?')[:6]

	context = {
		'alerta' : None,
		'imoveis': imoveis,
	}

	return render(request, 'home.html', context)

def imovel(request, pk):

	imovel = Imoveis.objects.get(pk=pk)

	context = {
		'imovel': imovel,
	}

	return render(request, 'imovel.html', context)

# View cadastro
def cadastro(request):

	context = {
		'alerta' : None,
	}

	if request.method == 'POST':
		form = RegisterForm(request.POST)

		if form.is_valid():

			username    = form.cleaned_data['email']
			email       = form.cleaned_data['email']
			nome        = form.cleaned_data['nome']
			telefone    = form.cleaned_data['telefone']
			senha		= form.cleaned_data['password1']

			obj_novo_usuario = User()

			obj_novo_usuario.username    = username
			obj_novo_usuario.email       = email
			obj_novo_usuario.nome        = nome
			obj_novo_usuario.telefone    = telefone
			obj_novo_usuario.set_password(senha)

			try:
				obj_novo_usuario.save()
			except:
				print_erro('Falha ao gravar objeto usuário')
				raise Http404

			return redirect('app:home')

	else:

		form = RegisterForm()

	context['form'] = form

	return render(request, 'cadastro.html', context)

def lista_imoveis(request):

	context = {
		'alerta' : None,
	}

	user = request.user

	if request.method == 'POST':

		titulo      = request.POST.get('titulo')
		valor       = request.POST.get('valor')
		cep         = request.POST.get('cep')
		logradouro  = request.POST.get('logradouro')
		numero      = request.POST.get('numero')
		complemento = request.POST.get('complemento')
		bairro      = request.POST.get('bairro')
		cidade      = request.POST.get('cidade')
		uf          = request.POST.get('uf')
		telefone    = request.POST.get('telefone')
		obs         = request.POST.get('obs')
		arquivo     = request.FILES['docfile']

		valor = valor.replace(',', '.')
		valor = Decimal(valor)

		# cria objeto imóvel

		obj_imoveis = Imoveis()

		obj_imoveis.titulo       = titulo
		obj_imoveis.valor        = valor
		obj_imoveis.logradouro   = logradouro
		obj_imoveis.numero       = numero
		obj_imoveis.complemento  = complemento
		obj_imoveis.bairro       = bairro
		obj_imoveis.cidade       = cidade
		obj_imoveis.uf           = uf
		obj_imoveis.cep          = cep
		obj_imoveis.telefone     = telefone
		obj_imoveis.observacoes  = obs
		obj_imoveis.usuario      = user
		obj_imoveis.arquivo      = arquivo
		obj_imoveis.nome_arquivo = arquivo.name

		try:
			obj_imoveis.save()
			context['alerta'] = 1
		except Exception as e:
			print_erro('Falha ao gravar objeto imóvel sob erro {0}'.format(e))
			context['alerta'] = 2

	# Retorna lista de imóveis

	obj_lista = Imoveis.objects.filter(usuario__pk=user.pk)

	if not len(obj_lista) > 0: obj_lista = None

	context['lista'] = obj_lista

	return render(request, 'lista.html', context)

def lista_imoveis_deleta(request, pk):

	obj_imovel = Imoveis.objects.get(pk=pk)
	obj_imovel.delete()

	return redirect('app:listaImoveis')
