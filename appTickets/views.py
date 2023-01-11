from django.shortcuts import render
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

# Create your views here.
def index(request):
    teste = getTickets()

    print(teste)

    dados = {
        'teste': teste
    }

    return render(request, 'index.html', dados)