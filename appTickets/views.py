from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db import connection
from datetime import datetime
from django.utils import timezone

def dictfetchall(cur): 
    desc = cur.description 
    return [
        dict(zip([col[0] for col in desc], row)) 
        for row in cur.fetchall() 
    ] 

def getTickets():
    sql = f"""select * from tickets order by cod_ticket desc
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
                t.data_inicio as data_inicio_original,
                t.data_fim as data_fim_original,
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
            left join operador_ticket ot
                on ot.tickets_cod_ticket = t.cod_ticket
            left join operador o
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
def setTicket(cod_ticket:int, desc_problema, cpf:str, data_inicio, data_fim: datetime):
    sql = f"""INSERT INTO tickets (cod_ticket, desc_problema, usuario_cpf, data_inicio, data_fim)
            VALUES ({cod_ticket}, '{desc_problema}', "{cpf}", "{data_inicio}", "{data_fim}"); 
            """        
    with connection.cursor() as cursor:
        try:
            cursor.execute(sql)
            cursor.close()
            return 
        except Exception as e:
            cursor.close() 

def setInfra(sistema_op, servidor:str, porta_switch,cod_ticket:int, ):
    sql = f"""INSERT INTO infra (sistema_op, servidor, porta_switch, tickets_cod_ticket)
            VALUES ('{sistema_op}', "{servidor}", {porta_switch}, {cod_ticket}); 
            """ 
    with connection.cursor() as cursor:
        try:
            cursor.execute(sql)
            cursor.close()
            return 
        except Exception as e:
            cursor.close()  

def setHospEmail(endereco_email, plano_hospedagem, solucao :str,cod_ticket:int):
    sql = f"""INSERT INTO hospedagem_email (endereco_emal, solucao, plano_hospedagem, tickets_cod_ticket)
            VALUES ('{endereco_email}', "{solucao}", "{plano_hospedagem}", {cod_ticket}); 
            """ 
    with connection.cursor() as cursor:
        try:
            cursor.execute(sql)
            cursor.close()
            return 
        except Exception as e:
            cursor.close()   

def setHospSite(dominio, plano_hospedagem, solucao :str,cod_ticket:int):
    sql = f"""INSERT INTO hospedagem_site (dominio, solucao, plano_hospedagem, tickets_cod_ticket)
            VALUES ('{dominio}', "{solucao}", "{plano_hospedagem}", {cod_ticket}); 
            """ 
    with connection.cursor() as cursor:
        try:
            cursor.execute(sql)
            cursor.close()
            return 
        except Exception as e:
            cursor.close() 

def setCloud(id_vm:int, servico, end_ip :str, cod_ticket:int):
    sql = f"""INSERT INTO cloud (id_vm, end_ip, servico, tickets_cod_ticket)
            VALUES ({id_vm}, "{end_ip}", "{servico}", {cod_ticket}); 
            """ 
    with connection.cursor() as cursor:
        try:
            cursor.execute(sql)
            cursor.close()
            return 
        except Exception as e:
            cursor.close() 

def setOperadorTicket(cod_ticket, operador_matricula:int):
    sql = f"""INSERT INTO operador_ticket (operador_matricula, tickets_cod_ticket)
            VALUES ({operador_matricula}, {cod_ticket}); 
            """ 
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
    cod_ticket = request.POST.get('cod_ticket')
    desc_problema = request.POST.get('desc_problema')
    data_inicio = request.POST.get('data_inicio')
    data_fim = request.POST.get('data_fim')
    cpf = request.POST.get('cpf')

    data_inicio = datetime.strptime(data_inicio, '%Y-%m-%dT%H:%M')
    data_fim = datetime.strptime(data_fim, '%Y-%m-%dT%H:%M')

    data_inicio = timezone.make_aware(data_inicio)
    data_fim = timezone.make_aware(data_fim)

    data_i = timezone.localtime(data_inicio)
    data_f = timezone.localtime(data_fim)

    setTicket(cod_ticket, desc_problema, cpf, data_i, data_f )

    tipo = request.POST.get('tipo')

    input1 = request.POST.get('input1')
    input2 = request.POST.get('input2')
    input3 = request.POST.get('input3')

    if tipo == 'infra':
        print("Infra")
        setInfra(input1, input2, input3, cod_ticket)
    elif tipo == 'email':
        print("E-mail")
        setHospEmail(input1, input2, input3, cod_ticket)
    elif tipo == 'site':
        print("Site")
        setHospSite(input1, input2, input3, cod_ticket)
    elif tipo == 'cloud':
        print("Cloud")
        setCloud(input1, input2, input3, cod_ticket)

    cnpj = request.POST.get('cnpj')
    matricula = request.POST.get('matricula')

    setOperadorTicket(cod_ticket, matricula)

    return redirect('/tickets')   

# ------------UPDATE---------------
def updateTicket(cod_ticket:int, desc_problema:str):
    sql = f"""update tickets set desc_problema = "{desc_problema}" where cod_ticket = {cod_ticket}; 
            """ 
    print(sql)       
    with connection.cursor() as cursor:
        try:
            cursor.execute(sql)
            cursor.close()
            return 
        except Exception as e:
            cursor.close()  

def updateInfra(sistema_op, servidor:str, porta_switch, cod_ticket:int, ):
    sql = f"""update infra set sistema_op = '{sistema_op}', servidor = "{servidor}", porta_switch = {porta_switch}
            where tickets_cod_ticket = {cod_ticket}; 
            """ 
    print(sql)
    with connection.cursor() as cursor:
        try:
            cursor.execute(sql)
            cursor.close()
            return 
        except Exception as e:
            cursor.close()  

def updateHospEmail(endereco_email, plano_hospedagem, solucao :str,cod_ticket:int):
    sql = f"""update hospedagem_email set endereco_emal = '{endereco_email}', solucao = "{solucao}",
        plano_hospedagem = "{plano_hospedagem}" where tickets_cod_ticket = {cod_ticket}
            """ 
    print(sql)
    with connection.cursor() as cursor:
        try:
            cursor.execute(sql)
            cursor.close()
            return 
        except Exception as e:
            cursor.close()   

def updateHospSite(dominio, plano_hospedagem, solucao :str,cod_ticket:int):
    sql = f"""update hospedagem_site set dominio = '{dominio}', solucao = "{solucao}", 
        plano_hospedagem = "{plano_hospedagem}" where tickets_cod_ticket = {cod_ticket}
            """ 
    print(sql)
    with connection.cursor() as cursor:
        try:
            cursor.execute(sql)
            cursor.close()
            return 
        except Exception as e:
            cursor.close() 

def updateCloud(id_vm:int, servico, end_ip :str, cod_ticket:int):
    sql = f"""update cloud set id_vm = {id_vm}, end_ip = "{end_ip}", servico = "{servico}"
        where tickets_cod_ticket = {cod_ticket}; 
            """ 
    print(sql)
    with connection.cursor() as cursor:
        try:
            cursor.execute(sql)
            cursor.close()
            return 
        except Exception as e:
            cursor.close() 


def salvarTicket(request):
    cod_ticket = request.POST.get('code')
    desc_problema = request.POST.get('desc_problema')
   
    updateTicket(cod_ticket, desc_problema )

    tipo = request.POST.get('tipo')

    input1 = request.POST.get('input1')
    input2 = request.POST.get('input2')
    input3 = request.POST.get('input3')

    if tipo == 'Infra':
        print("Infra")
        updateInfra(input1, input2, input3, cod_ticket)
    elif tipo == 'Email':
        print("E-mail")
        updateHospEmail(input1, input2, input3, cod_ticket)
    elif tipo == 'Site':
        print("Site")
        updateHospSite(input1, input2, input3, cod_ticket)
    elif tipo == 'Cloud':
        print("Cloud")
        updateCloud(input1, input2, input3, cod_ticket)

    return redirect('/tickets')   

def editaTicket(request):
    cod_ticket = request.POST.get('cod_ticket')

    ticket = getTicketCode(cod_ticket)
    tipo = ''

    print(ticket)
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
    return render(request, 'editaTicket.html', dados)

# ------------DELETE---------------
def deleteTicket(cod_ticket:str):
    sql = f"""delete from tickets where cod_ticket = {cod_ticket}; 
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

# ------------ENUNCIADOS---------------
def enunciados(request):
    """ res = getEmpresaCliente()

    dados = {
        'lista': res
    } """

    return render(request, 'enunciados.html')

def verEnunciado01(request):
    res = executaEnunciado01()

    dados = {
        'lista': res
    }

    return render(request, 'verEnunciado01.html', dados)

def verEnunciado02(request):
    res = executaEnunciado02()

    dados = {
        'lista': res
    }

    return render(request, 'verEnunciado02.html', dados)

def verEnunciado03(request):
    res = executaEnunciado03()

    dados = {
        'lista': res
    }

    return render(request, 'verEnunciado03.html', dados)

def verEnunciado04(request):
    res = executaEnunciado04()

    dados = {
        'lista': res
    }

    return render(request, 'verEnunciado04.html', dados)

def verEnunciado05(request):
    res = executaEnunciado05()

    dados = {
        'lista': res
    }

    return render(request, 'verEnunciado05.html', dados)

def verEnunciado06(request):
    res = executaEnunciado06()

    dados = {
        'lista': res
    }

    return render(request, 'verEnunciado06.html', dados)

def verEnunciado07(request):
    res = executaEnunciado07()

    dados = {
        'lista': res
    }

    return render(request, 'verEnunciado07.html', dados)

def verEnunciado08(request):
    res = executaEnunciado08()

    dados = {
        'lista': res
    }

    return render(request, 'verEnunciado08.html', dados)

def verEnunciado09(request):
    res = executaEnunciado09()

    dados = {
        'lista': res
    }

    return render(request, 'verEnunciado09.html', dados)

def verEnunciado10(request):
    res = executaEnunciado10()

    dados = {
        'lista': res
    }

    return render(request, 'verEnunciado10.html', dados)

def executaEnunciado01():
    sql = f"""SELECT o.nome, count(ot.tickets_cod_ticket) AS quantidade
                    FROM operador o INNER JOIN operador_ticket ot	ON o.matricula = ot.operador_matricula
                    GROUP BY 1; 
            """        
    with connection.cursor() as cursor:
        try:
            cursor.execute(sql)
            rs =  dictfetchall(cursor)
            cursor.close()
            return rs 
        except Exception as e:
            cursor.close()   

def executaEnunciado02():
    sql = f"""select empresa_cliente.nome, COUNT(tickets.cod_ticket) AS quantidade from empresa_cliente
                    inner join usuario
                    on empresa_cliente.cnpj=usuario.empresa_cliente_cnpj
                    INNER JOIN tickets
                    ON tickets.usuario_cpf=usuario.cpf
                    GROUP BY empresa_cliente.nome
                    HAVING COUNT(tickets.cod_ticket)=
                    (SELECT MAX(n.t) from (select empresa_cliente.nome,  COUNT(tickets.cod_ticket) as t from empresa_cliente
                    inner join usuario
                    on empresa_cliente.cnpj=usuario.empresa_cliente_cnpj
                    INNER JOIN tickets
                    ON tickets.usuario_cpf=usuario.cpf
                    GROUP BY empresa_cliente.nome) as n);
            """        
    with connection.cursor() as cursor:
        try:
            cursor.execute(sql)
            rs =  dictfetchall(cursor)
            cursor.close()
            return rs 
        except Exception as e:
            cursor.close()   

def executaEnunciado03():
    sql = f"""SELECT usuario.nome from usuario
                    WHERE usuario.cpf NOT IN (SELECT tickets.usuario_cpf from tickets
                    WHERE tickets.cod_ticket in (SELECT hospedagem_email.tickets_cod_ticket FROM hospedagem_email));
            """        
    with connection.cursor() as cursor:
        try:
            cursor.execute(sql)
            rs =  dictfetchall(cursor)
            cursor.close()
            return rs 
        except Exception as e:
            cursor.close()   

def executaEnunciado04():
    sql = f"""SELECT
                    (SELECT COUNT(hospedagem_email.tickets_cod_ticket)  FROM hospedagem_email) as he,
                    (SELECT COUNT(hospedagem_site.tickets_cod_ticket) FROM hospedagem_site) as hs, 
                    (SELECT COUNT(infra.tickets_cod_ticket) FROM infra) as infra, 
                    (SELECT COUNT(cloud.tickets_cod_ticket) FROM cloud) as cloud; 
            """        
    with connection.cursor() as cursor:
        try:
            cursor.execute(sql)
            rs =  dictfetchall(cursor)
            cursor.close()
            return rs 
        except Exception as e:
            cursor.close()   

def executaEnunciado05():
    sql = f"""SELECT n.nome, n.operador, MAX(n.t) as tickets FROM (select operador.nome as operador, empresa_cliente.nome, COUNT(tickets.cod_ticket) as t 
                	from empresa_cliente
	                inner join usuario
		            on empresa_cliente.cnpj=usuario.empresa_cliente_cnpj
	                INNER JOIN tickets
		            ON tickets.usuario_cpf=usuario.cpf
	                INNER JOIN operador_ticket
		            ON operador_ticket.tickets_cod_ticket=tickets.cod_ticket                    
	                INNER JOIN operador
		            ON operador.matricula=operador_ticket.operador_matricula                       
	                GROUP BY 1,2) as n
                    GROUP BY n.nome;
            """        
    with connection.cursor() as cursor:
        try:
            cursor.execute(sql)
            rs =  dictfetchall(cursor)
            cursor.close()
            return rs 
        except Exception as e:
            cursor.close()   

def executaEnunciado06():
    sql = f"""SELECT n.nome, n.operador, MAX(n.t) as tickets FROM (select operador.nome as operador, empresa_cliente.nome, COUNT(tickets.cod_ticket) as t 
                	from empresa_cliente
	                inner join usuario
		            on empresa_cliente.cnpj=usuario.empresa_cliente_cnpj
	                INNER JOIN tickets
		            ON tickets.usuario_cpf=usuario.cpf
	                INNER JOIN operador_ticket
		            ON operador_ticket.tickets_cod_ticket=tickets.cod_ticket                    
	                INNER JOIN operador
		            ON operador.matricula=operador_ticket.operador_matricula                       
	                GROUP BY 1,2) as n
                    GROUP BY n.nome;

            """        
    with connection.cursor() as cursor:
        try:
            cursor.execute(sql)
            rs =  dictfetchall(cursor)
            cursor.close()
            return rs 
        except Exception as e:
            cursor.close()   

def executaEnunciado07():
    sql = f"""SELECT empresa_cliente.nome as Empresa, usuario.nome as Usuario, operador.nome as Operador, tickets.data_inicio, tickets.data_fim FROM empresa_cliente
                    INNER JOIN usuario
                    ON usuario.empresa_cliente_cnpj=empresa_cliente.cnpj
                    INNER JOIN tickets
                    ON tickets.usuario_cpf=usuario.cpf
                    INNER JOIN operador_ticket
                    ON operador_ticket.tickets_cod_ticket=tickets.cod_ticket
                    INNER JOIN operador
                    ON operador.matricula=operador_ticket.operador_matricula
                    GROUP BY empresa_cliente.nome
                    HAVING  DATEDIFF(tickets.data_inicio, tickets.data_fim) =
                    (SELECT MIN(d.dif) FROM (SELECT DATEDIFF(tickets.data_inicio,tickets.data_fim) AS dif FROM tickets )as d);
            """        
    with connection.cursor() as cursor:
        try:
            cursor.execute(sql)
            rs =  dictfetchall(cursor)
            cursor.close()
            return rs 
        except Exception as e:
            cursor.close()   

def executaEnunciado08():
    sql = f"""select infra.sistema_op, COUNT(infra.sistema_op) as tickets from infra
                    GROUP BY infra.sistema_op
                    HAVING COUNT(infra.sistema_op)=
                    (SELECT MAX(i.sis) FROM (SELECT COUNT(infra.sistema_op) AS sis FROM infra GROUP BY infra.sistema_op)as i); 
            """        
    with connection.cursor() as cursor:
        try:
            cursor.execute(sql)
            rs =  dictfetchall(cursor)
            cursor.close()
            return rs 
        except Exception as e:
            cursor.close()   

def executaEnunciado09():
    sql = f"""SELECT n.nome, count(usuario.cpf) as usuarios, n.t as tickets FROM (select empresa_cliente.nome, empresa_cliente.cnpj, COUNT(tickets.cod_ticket) as t 
                	from empresa_cliente
	                inner join usuario
		            on empresa_cliente.cnpj=usuario.empresa_cliente_cnpj
	                INNER JOIN tickets
		            ON tickets.usuario_cpf=usuario.cpf
	                GROUP BY 1) as n
                    INNER JOIN usuario
	                ON usuario.empresa_cliente_cnpj=n.cnpj
                    GROUP BY n.nome; 
            """        
    with connection.cursor() as cursor:
        try:
            cursor.execute(sql)
            rs =  dictfetchall(cursor)
            cursor.close()
            return rs 
        except Exception as e:
            cursor.close()   

def executaEnunciado10():
    sql = f"""select usuario.nome, count(tickets.cod_ticket) as tickets from usuario
inner join tickets
on usuario.cpf=tickets.usuario_cpf
group by usuario.nome;
 
            """        
    with connection.cursor() as cursor:
        try:
            cursor.execute(sql)
            rs =  dictfetchall(cursor)
            cursor.close()
            return rs 
        except Exception as e:
            cursor.close()   

