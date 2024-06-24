from django.shortcuts import render
from django.db import connection

# Create your views here.
def mostrarReuniones(request):
    query="SELECT Asunto_Reunion, Fecha_Reunion, Hora_Reunion FROM Reunion;"

    with connection.cursor() as cursor:
        cursor.execute(query)
        reuniones=cursor.fetchall()
    
    context={
        "reuniones":reuniones
    }

    return render(request,'reunionesBase.html',context)