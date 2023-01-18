from django.urls import path

from . import views

urlpatterns = [
    path('', views.tickets, name='tickets'),
    path('tickets', views.tickets, name='tickets'),
    path('cadastrarTicket', views.cadastraTicket, name='cadastrarTicket'),
    path('salvarNovoTicket', views.salvarNovoTicket, name='salvarNovoTicket'),
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
]