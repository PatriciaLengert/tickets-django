from django.urls import path

from . import views

urlpatterns = [
    path('', views.tickets, name='tickets'),
    path('tickets', views.tickets, name='tickets'),
    path('cadastrarTicket', views.cadastraTicket, name='cadastrarTicket'),
    path('salvarNovoTicket', views.salvarNovoTicket, name='salvarNovoTicket'),
    path('editaTicket', views.editaTicket, name='editaTicket'),
    path('salvarTicket', views.salvarTicket, name='salvarTicket'),
    path('verTicket', views.verTickets, name='verTicket'),
    path('deletaTicket', views.deletaTicket, name='deletaTicket'),
    #empresa
    path('empresasClientes', views.empresaCliente, name='empresasClientes'),
    path('cadastraEmpresa', views.cadastraEmpresaCliente, name='cadastraEmpresa'),
    path('editaEmpresa', views.editaEmpresaCliente, name='editaEmpresa'),
    path('salvarEmpresa', views.salvarEmpresaCliente, name='salvarEmpresa'),
    path('deletaEmpresa', views.deletaEmpresaCliente, name='deletaEmpresa'),
    #usuario
    path('usuariosEmpresa', views.usuariosEmpresa, name='usuariosEmpresa'),
    path('cadastraUsuario', views.cadastraUsuario, name='cadastraUsuario'),
    path('editaUsuario', views.editaUsuario, name='editaUsuario'),
    path('salvarUsuario', views.salvarUsuario, name='salvarUsuario'),
    path('deletaUsuario', views.deletaUsuario, name='deletaUsuario'),
    #operador
    path('operador', views.operador, name='operador'),
    path('cadastraOperador', views.cadastraOperador, name='cadastraOperador'),
    path('editaOperador', views.editaOperador, name='editaOperador'),
    path('salvarOperador', views.salvarOperador, name='salvarOperador'),
    path('deletaOperador', views.deletaOperador, name='deletaOperador'),
    #enunciados
    path('enunciados', views.enunciados, name='enunciados'),
    path('verEnunciado01', views.verEnunciado01, name='verEnunciado01'),
    path('verEnunciado02', views.verEnunciado02, name='verEnunciado02'),
    path('verEnunciado03', views.verEnunciado03, name='verEnunciado03'),
    path('verEnunciado04', views.verEnunciado04, name='verEnunciado04'),
    path('verEnunciado05', views.verEnunciado05, name='verEnunciado05'),
    path('verEnunciado06', views.verEnunciado06, name='verEnunciado06'),
    path('verEnunciado07', views.verEnunciado07, name='verEnunciado07'),
    path('verEnunciado08', views.verEnunciado08, name='verEnunciado08'),
    path('verEnunciado09', views.verEnunciado09, name='verEnunciado09'),
    path('verEnunciado10', views.verEnunciado10, name='verEnunciado10'),
]