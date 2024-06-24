from django.shortcuts import render,redirect
from .models import Tipo_Cuestionario
from django.db import connection

# Create your views here.
def crear(request):
    with connection.cursor() as cursor:
        cursor.execute('SELECT ID_Tipo_Cuestionario, Tipo FROM Tipo_Cuestionario;')
        tiposCuestionario = cursor.fetchall()

    return render(request,'crear.html',{"tiposCuestionario":tiposCuestionario})

def botonCrear(request):
    id_especialista=request.POST['id_especialista']
    id_tipo_cuestionario=request.POST['id_tipo_cuestionario']

    query=f"INSERT INTO Cuestionario(ID_Cuestionario,ID_Especialista_Relaciones_Laborales,ID_Tipo_Cuestionario,Fecha_Creacion,Hora_Creacion,ID_Estado_Envio,Fecha_Envio_Gerencia,Hora_Envio_Gerencia,ID_Gerente,ID_Estado_Aprobacion,Fecha_Revision,Hora_Revision) VALUES (CASE WHEN (SELECT MAX(ID_Cuestionario) FROM Cuestionario) IS NULL THEN 1 ELSE (SELECT MAX(ID_Cuestionario) FROM Cuestionario) + 1 END, {id_especialista},{id_tipo_cuestionario},CURRENT_DATE,CURRENT_TIME(0),2,NULL,NULL,20200001,2,NULL,NULL);"

    with connection.cursor() as cursor:
            cursor.execute(query)

    return redirect('/crear/')