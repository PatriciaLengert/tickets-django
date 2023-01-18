from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db import connection
from datetime import datetime

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

def tickets(request):
    ticket = getTickets()

    #print(ticket)

    dados = {
        'lista': ticket
    }

    return render(request, 'tickets.html', dados)

def getTicketCode(code:int):
    sql = f"""SELECT 
                t.cod_ticket,
                t.desc_problema,
                date_format(t.data_inicio, '%d/%m/%Y %H:%i') as data_inicio,
                date_format(t.data_fim, '%d/%m/%Y %H:%i') as data_fim,
                u.cpf,
                u.nome as nome_usuario,
                u.cargo as cargo_usuario,
                u.setor as setor_usuario,
                o.matricula,
                o.nome as operador,
                o.cargo as cargo_operador,
                o.telefone as telefone_operador,
                ec.cnpj,
                ec.nome as empresa_cliente,
                ec.endereco,
                ec.telefone as telefone_empresa,
                i.*, 
                hs.dominio as site_dominio,
                hs.plano_hospedagem as site_plano_hospedagem,
                hs.solucao as site_solucao,
                he.endereco_emal,  
                he.plano_hospedagem as email_plano_hospedagem,
                he.solucao as email_solucao,
                c.*
            FROM tickets t
            inner join operador_ticket ot
                on ot.tickets_cod_ticket = t.cod_ticket
            inner join operador o
                on ot.operador_matricula = o.matricula
            inner join usuario u
                on u.cpf = t.usuario_cpf
            inner join empresa_cliente ec
                on ec.cnpj = u.empresa_cliente_cnpj
            left join infra i
                on t.cod_ticket = i.tickets_cod_ticket
            left join hospedagem_site hs
                on t.cod_ticket = hs.tickets_cod_ticket
            left join hospedagem_email he
                on t.cod_ticket = he.tickets_cod_ticket
            left join cloud as c
                on t.cod_ticket = c.tickets_cod_ticket
            where cod_ticket = {code}
            order by cod_ticket
            """        
    with connection.cursor() as cursor:
        try:
            cursor.execute(sql)
            rs =  dictfetchall(cursor)
            cursor.close()
            return rs
        except Exception as e:
            cursor.close()

def verTickets(request):
    code = request.POST.get('code')

    ticket = getTicketCode(code)
    tipo = ''

    for t in ticket:
        if t['endereco_emal'] != None:
            tipo = 'Email'
        elif t['site_dominio'] != None:
            tipo = 'Site'
        elif t['sistema_op'] != None:
            tipo = 'Infra'
        elif t['end_ip'] != None:
            tipo = 'Cloud'
        else:
            tipo = 'ST'
    
    dados = {
        'ticket': ticket,
        'tipo': tipo
    }

    return render(request, 'verTicket.html', dados)

# ------------INSERT---------------
def setTicket(desc_problema, cpf:str, data_inicio, data_fim: datetime):
    sql = f"""INSERT INTO tickets (desc_problema, cpf, data_inicio, data_fim, )
            VALUES ('{desc_problema}', "{cpf}", "{data_inicio}", "{data_fim}", ); 
            """        
    print(sql)
    with connection.cursor() as cursor:
        try:
            cursor.execute(sql)
            cursor.close()
            return 
        except Exception as e:
            cursor.close()   

def cadastraTicket(request):
    return render(request, 'cadastrarTicket.html')

def salvarNovoTicket(request):
    desc_problema = request.POST.get('desc_problema')
    data_inicio = request.POST.get('data_inicio')
    data_fim = request.POST.get('data_fim')
    cpf = request.POST.get('cpf')

    data_i = datetime.strptime(data_inicio, "%Y-%m-%d %H:%M:%S").date()

    data_f = datetime.strptime(data_fim, "%Y-%m-%d %H:%M:%S").date()

    print(data_inicio)
    setTicket(desc_problema, cpf, data_i, data_f )

    infra = request.POST.get('infra')
    email = request.POST.get('email')
    site = request.POST.get('site')
    cloud = request.POST.get('cloud')

    input1 = request.POST.get('input1')
    input2 = request.POST.get('input2')
    input3 = request.POST.get('input3')

    cnpj = request.POST.get('cnpj')
    matricula = request.POST.get('matricula')

    return render(request, 'cadastrarTicket.html')   

# ------------DELETE---------------
def deleteTicket(cod_ticket:str):
    sql = f"""delete from ticket where cod_ticket = '{cod_ticket}'; 
            """        
    with connection.cursor() as cursor:
        try:
            cursor.execute(sql)
            cursor.close()
            return 
        except Exception as e:
            cursor.close()   

def deletaTicket(request):
    cod_ticket = request.POST.get('cod_ticket')

    deleteTicket(cod_ticket)

    return redirect('/tickets')

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

    res = getUsuarioEmpresa(cnpj)

    dados = {
        'lista': res,
        'cnpj': cnpj
    }

    return render(request, 'usuariosEmpresa.html', dados)

# ------------UPDATE---------------
def updateUsuario(cpf, nome, cargo, setor:str):
    sql = f"""update usuario set nome = "{nome}", cargo = "{cargo}", setor = "{setor}" where cpf = '{cpf}'; 
            """        
    with connection.cursor() as cursor:
        try:
            cursor.execute(sql)
            cursor.close()
            return 
        except Exception as e:
            cursor.close()   

def getUsuarioUpdate(cpf:str):
    sql = f"""select * from usuario where cpf = '{cpf}'
            """        
    with connection.cursor() as cursor:
        try:
            cursor.execute(sql)
            rs =  dictfetchall(cursor)
            cursor.close()
            return rs
        except Exception as e:
            cursor.close()

def editaUsuario(request):
    cpf = request.POST.get('cpf')
    cnpj = request.POST.get('cnpj')

    res = getUsuarioUpdate(cpf)

    dados = {
        'lista': res,
        'cnpj': cnpj
    }

    return render(request, 'editaUsuario.html', dados)

def salvarUsuario(request):
    cpf = request.POST.get('cpf')
    nome = request.POST.get('nome')
    cargo = request.POST.get('cargo')
    setor = request.POST.get('setor')
    cnpj = request.POST.get('cnpj')

    updateUsuario(cpf, nome, cargo, setor)

    res = getUsuarioEmpresa(cnpj)

    dados = {
        'lista': res,
        'cnpj': cnpj
    }

    return render(request, 'usuariosEmpresa.html', dados)


# ------------DELETE---------------
def deleteUsuario(cpf:str):
    sql = f"""delete from usuario where cpf = '{cpf}'; 
            """        
    with connection.cursor() as cursor:
        try:
            cursor.execute(sql)
            cursor.close()
            return 
        except Exception as e:
            cursor.close()   

def deletaUsuario(request):
    cpf = request.POST.get('cpf')
    cnpj = request.POST.get('cnpj')

    deleteUsuario(cpf)

    res = getUsuarioEmpresa(cnpj)

    dados = {
        'lista': res,
        'cnpj': cnpj
    }

    return render(request, 'usuariosEmpresa.html', dados)

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