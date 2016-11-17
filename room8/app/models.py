'''
app.models.py

Arquivo responsável pelo ORM das classes da aplicação junto ao
banco de dados.
'''

from __future__ import unicode_literals
import django.utils.timezone
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.conf import settings

# Classe usuário

class ModUserManager(UserManager):

    def get_usuario(self, pk):
        try:
            registro = self.get_queryset().get(pk=pk)
            return registro
        except User.DoesNotExist:
            return False

class User(AbstractBaseUser, PermissionsMixin):
    username    = models.CharField('Username', max_length=100, blank=True, null=False)
    email       = models.EmailField('e-Mail', max_length=100, null=True, blank=False, unique=True)
    nome        = models.CharField('Nome', max_length=100, null=True, blank=False)
    telefone    = models.CharField('Contato', max_length=15, null=True, blank=False)
    is_active   = models.BooleanField('Ativo?', default=True)
    is_staff    = models.BooleanField('É Admin?', default=False)
    date_joined = models.DateTimeField('Criado em', auto_now_add=True)

    # Classe responsavel por operar
    objects = ModUserManager()

    # CAMPO BASE PARA LOGIN
    USERNAME_FIELD = 'email'

    # CAMPO PADRAO PARA CRIAÇÃO DE SUPERUSUARIOS
    REQUIRED_FIELDS = ['username', 'nome']

    def __str__(self):
        return self.nome or self.username

    def get_short_name(self):
        return self.nome

    def get_full_name(self):
        return str(self)

    class Meta:
        verbose_name        = 'Usuário'
        verbose_name_plural = 'Usuários'

# Classe Imóveis

class Imoveis(models.Model):
    titulo       = models.CharField('Título', max_length=255, null=True, blank=False)
    valor        = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=False)
    logradouro   = models.CharField('Logradouro', max_length=200, null=True, blank=False)
    numero       = models.CharField('Número', max_length=50, null=True, blank=False)
    complemento  = models.CharField('Complemento', max_length=50, null=True, blank=True)
    bairro       = models.CharField('Bairro', max_length=100, null=True, blank=False)
    cidade       = models.CharField('Cidade', max_length=100, null=True, blank=False)
    uf           = models.CharField('UF', max_length=2, null=True, blank=False)
    cep          = models.CharField('CEP', max_length=9, null=True, blank=False)
    telefone     = models.CharField('Contato', max_length=15, null=True, blank=False)
    observacoes  = models.TextField()
    lat          = models.CharField('Latitude', max_length=50, null=True, blank=True)
    lon          = models.CharField('Longitude', max_length=50, null=True, blank=True)
    arquivo      = models.FileField(upload_to='imgs/', blank = True, null= True)
    nome_arquivo = models.CharField(max_length=255, blank = True, null= True)
    usuario      = models.ForeignKey('User', on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name        = 'Imóvel'
        verbose_name_plural = 'Imóveis'

# Classe Mensagens

class Mensagens(models.Model):
    texto       = models.TextField()
    dt_criacao  = models.DateTimeField('Criada em', auto_now_add=True, blank = True, null= True)
    imovel      = models.ForeignKey('Imoveis', on_delete=models.DO_NOTHING)
    postado_por = models.ForeignKey('User', on_delete=models.DO_NOTHING, blank=True, null=True)
    resposta    = models.ForeignKey('Mensagens', on_delete=models.DO_NOTHING, blank=True, null=True)

    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name        = 'Mensagem'
        verbose_name_plural = 'Mensagens'
