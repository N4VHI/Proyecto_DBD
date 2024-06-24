from django.shortcuts import render,redirect
from django.db import connection

# Create your views here.
def baseProgramarReunion(request):
    return render(request,'baseProgramarReunion.html')

def botonProgramar(request):
    id_organizador=request.POST['id_organizador']
    asunto=request.POST['asunto']
    fecha=request.POST['fecha']
    hora=request.POST['hora']

    query=" INSERT INTO Reunion (ID_Reunion, ID_Organizador, Asunto_Reunion, Fecha_Reunion, Hora_Reunion) VALUES (CASE WHEN (SELECT MAX(ID_Reunion) FROM Reunion) IS NULL THEN 1 ELSE (SELECT MAX(ID_Reunion) FROM Reunion) + 1 END,%s, %s, %s,%s);"

    with connection.cursor() as cursor:
        cursor.execute(query,[id_organizador,asunto,fecha,hora])

    return redirect('/programarReunion/')


