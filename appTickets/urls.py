from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('empresasClientes', views.empresaCliente, name='empresasClientes'),
    path('cadastraEmpresa', views.cadastraEmpresaCliente, name='cadastraEmpresa'),
    path('editaEmpresa', views.editaEmpresaCliente, name='editaEmpresa'),
    path('salvarEmpresa', views.salvarEmpresaCliente, name='salvarEmpresa'),
    path('deletaEmpresa', views.deletaEmpresaCliente, name='deletaEmpresa'),
]