from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db import connection

def dictfetchall(cur): 
    desc = cur.description 
    return [
        dict(zip([col[0] for col in desc], row)) 
        for row in cur.fetchall() 
    ] 

def getTickets():
    sql = f"""select * from tickets
            """        
    with connection.cursor() as cursor:
        try:
            cursor.execute(sql)
            rs =  dictfetchall(cursor)
            cursor.close()
            return rs
        except Exception as e:
            cursor.close()

def index(request):
    teste = getTickets()

    #print(teste)

    dados = {
        'teste': teste
    }

    return render(request, 'index.html', dados)

# ----------Empresa cliente------------------

# ------------SELECT---------------
def getEmpresaCliente():
    sql = f"""select * from empresa_cliente order by nome
            """        
    with connection.cursor() as cursor:
        try:
            cursor.execute(sql)
            rs =  dictfetchall(cursor)
            cursor.close()
            return rs
        except Exception as e:
            cursor.close()

def empresaCliente(request):
    res = getEmpresaCliente()

    dados = {
        'lista': res
    }

    return render(request, 'empresaCliente.html', dados)

# ------------INSERT---------------
def setEmpresaCliente(cnpj, nome, endereco, telefone:str):
    sql = f"""INSERT INTO empresa_cliente (cnpj, nome, endereco, telefone)
            VALUES ('{cnpj}', "{nome}", "{endereco}", "{telefone}"); 
            """        
    with connection.cursor() as cursor:
        try:
            cursor.execute(sql)
            cursor.close()
            return 
        except Exception as e:
            cursor.close()   

def cadastraEmpresaCliente(request):
    cnpj = request.POST.get('cnpj')
    nome = request.POST.get('nome')
    endereco = request.POST.get('endereco')
    telefone = request.POST.get('telefone')

    setEmpresaCliente(cnpj, nome, endereco, telefone)

    return redirect('/empresasClientes')

# ------------UPDATE---------------
def updateEmpresaCliente(cnpj, nome, endereco, telefone:str):
    sql = f"""update empresa_cliente set nome = "{nome}", endereco = "{endereco}", telefone = "{telefone}" where cnpj = '{cnpj}'; 
            """        
    with connection.cursor() as cursor:
        try:
            cursor.execute(sql)
            cursor.close()
            return 
        except Exception as e:
            cursor.close()   

def getEmpresaClienteUpdate(cnpj:str):
    sql = f"""select * from empresa_cliente where cnpj = '{cnpj}'
            """        
    with connection.cursor() as cursor:
        try:
            cursor.execute(sql)
            rs =  dictfetchall(cursor)
            cursor.close()
            return rs
        except Exception as e:
            cursor.close()

def editaEmpresaCliente(request):
    cnpj = request.POST.get('cnpj')

    res = getEmpresaClienteUpdate(cnpj)

    dados = {
        'lista': res
    }

    return render(request, 'editaEmpresaCliente.html', dados)

def salvarEmpresaCliente(request):
    cnpj = request.POST.get('cnpj')
    nome = request.POST.get('nome')
    endereco = request.POST.get('endereco')
    telefone = request.POST.get('telefone')

    updateEmpresaCliente(cnpj, nome, endereco, telefone)

    return redirect('/empresasClientes')

# ------------DELETE---------------
def deleteEmpresaCliente(cnpj:str):
    sql = f"""delete from empresa_cliente where cnpj = '{cnpj}'; 
            """        
    with connection.cursor() as cursor:
        try:
            cursor.execute(sql)
            cursor.close()
            return 
        except Exception as e:
            cursor.close()   

def deletaEmpresaCliente(request):
    cnpj = request.POST.get('cnpj')

    deleteEmpresaCliente(cnpj)

    return redirect('/empresasClientes')

#----------------Usuário---------------    
# ------------SELECT---------------
def getUsuarioEmpresa(cnpj:str):
    sql = f"""select * from usuario where empresa_cliente_cnpj ='{cnpj}' order by nome
            """        
    with connection.cursor() as cursor:
        try:
            cursor.execute(sql)
            rs =  dictfetchall(cursor)
            cursor.close()
            return rs
        except Exception as e:
            cursor.close()

def usuariosEmpresa(request):
    cnpj = request.POST.get('cnpj')
    res = getUsuarioEmpresa(cnpj)

    dados = {
        'lista': res,
        'cnpj': cnpj
    }

    return render(request, 'usuariosEmpresa.html', dados)

#INSERT AINDA NÃO FUNCIONAAA---------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------

# ------------INSERT---------------
def setUsuario(cpf, nome, cargo, setor, cnpj:str):
    sql = f"""INSERT INTO usuario (cpf, nome, cargo, setor, empresa_cliente_cnpj)
            VALUES ('{cpf}', "{nome}", "{cargo}", "{setor}", "{cnpj}"); 
            """        
    with connection.cursor() as cursor:
        try:
            cursor.execute(sql)
            cursor.close()
            return 
        except Exception as e:
            cursor.close()   

def cadastraUsuario(request):
    cpf = request.POST.get('cpf')
    nome = request.POST.get('nome')
    cargo = request.POST.get('cargo')
    setor = request.POST.get('setor')
    cnpj = request.POST.get('cnpj')

    setUsuario(cpf, nome, cargo, setor, cnpj)

    return redirect('/usuariosEmpresa')

# ----------Operador------------------

# ------------SELECT---------------
def getOperador():
    sql = f"""select * from operador order by matricula
            """        
    with connection.cursor() as cursor:
        try:
            cursor.execute(sql)
            rs =  dictfetchall(cursor)
            cursor.close()
            return rs
        except Exception as e:
            cursor.close()

def operador(request):
    res = getOperador()

    dados = {
        'lista': res
    }

    return render(request, 'operador.html', dados)
    
# ------------INSERT---------------
def setOperador(matricula, nome, cargo, telefone:str):
    sql = f"""INSERT INTO operador (matricula, nome, cargo, telefone)
            VALUES ('{matricula}', "{nome}", "{cargo}", "{telefone}"); 
            """        
    with connection.cursor() as cursor:
        try:
            cursor.execute(sql)
            cursor.close()
            return 
        except Exception as e:
            cursor.close()   

def cadastraOperador(request):
    matricula = request.POST.get('matricula')
    nome = request.POST.get('nome')
    cargo = request.POST.get('cargo')
    telefone = request.POST.get('telefone')

    setOperador(matricula, nome, cargo, telefone)

    return redirect('/operador')

# ------------UPDATE---------------
def updateOperador(matricula, nome, cargo, telefone:str):
    sql = f"""update operador set nome = "{nome}", cargo = "{cargo}", telefone = "{telefone}" where matricula = '{matricula}'; 
            """  
    print(sql)      
    with connection.cursor() as cursor:
        try:
            cursor.execute(sql)
            cursor.close()
            return 
        except Exception as e:
            cursor.close()   

def getOperadorUpdate(matricula:str):
    sql = f"""select * from operador where matricula = '{matricula}'
            """        
    with connection.cursor() as cursor:
        try:
            cursor.execute(sql)
            rs =  dictfetchall(cursor)
            cursor.close()
            return rs
        except Exception as e:
            cursor.close()

def editaOperador(request):
    matricula = request.POST.get('matricula')

    res = getOperadorUpdate(matricula)

    dados = {
        'lista': res
    }

    return render(request, 'editaOperador.html', dados)

def salvarOperador(request):
    matricula = request.POST.get('matricula')
    nome = request.POST.get('nome')
    cargo = request.POST.get('cargo')
    telefone = request.POST.get('telefone')

    print(matricula)
    updateOperador(matricula, nome, cargo, telefone)

    return redirect('/operador')

# ------------DELETE---------------
def deleteOperador(matricula:str):
    sql = f"""delete from operador where matricula = '{matricula}'; 
            """        
    with connection.cursor() as cursor:
        try:
            cursor.execute(sql)
            cursor.close()
            return 
        except Exception as e:
            cursor.close()   

def deletaOperador(request):
    matricula = request.POST.get('matricula')

    deleteOperador(matricula)

    return redirect('/operador')