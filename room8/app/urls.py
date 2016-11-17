'''
app.urls.py

Arquivo responsável por gerenciar lógicas de respostas dentro da
aplicação 'app'.
'''

from django.conf.urls import url
from django.contrib.auth import views as djangoviews
from . import views

app_name = 'app'
urlpatterns = [
    url(r'^$', views.index, name='home'),
    url(r'^cadastro/$', views.cadastro, name='cadastro'),
    url(r'^lista/$', views.lista_imoveis, name='listaImoveis'),
    url(r'^lista/deleta/(?P<pk>\d+)/$', views.lista_imoveis_deleta, name='listaImoveisDeleta'),
    url(r'^imovel/(?P<pk>\d+)/$', views.imovel, name='imovel'),
    url(r'^login/$', djangoviews.login, {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', djangoviews.logout, {'next_page': 'app:home'}, name='logout'),
]
