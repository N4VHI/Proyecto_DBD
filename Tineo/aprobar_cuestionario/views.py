from django.shortcuts import render,redirect
from django.db import connection

# Create your views here.

def baseAprobar(request):
    with connection.cursor() as cursor:
        cursor.execute('SELECT ID_Tipo_Cuestionario, Tipo FROM Tipo_Cuestionario;')
        tiposCuestionario = cursor.fetchall()
    return render(request,'baseAprobar.html',{"tiposCuestionario":tiposCuestionario})


def mostrarPreguntas(request,id_tipo_cuestionario):
    with connection.cursor() as cursor:
        cursor.execute('SELECT ID_Tipo_Cuestionario, Tipo FROM Tipo_Cuestionario;')
        tiposCuestionario = cursor.fetchall()

    query=f"SELECT PC.ID_Pregunta, PC.Enunciado_Pregunta FROM Pregunta_Cuestionario PC INNER JOIN Cuestionario C ON PC.ID_Cuestionario = C.ID_Cuestionario WHERE C.ID_Tipo_Cuestionario = {id_tipo_cuestionario};"

    with connection.cursor() as cursor:
        cursor.execute(query)
        preguntas= cursor.fetchall()

    query=f"Select TE.Tipo as Estado_Envio from Cuestionario CU inner join Tipo_Estado TE on CU.Id_Estado_Envio=TE.Id_Tipo_Estado where Id_Tipo_Cuestionario={id_tipo_cuestionario};"

    with connection.cursor() as cursor:
        cursor.execute(query)
        estadoEnvio= cursor.fetchall()

    query=f"Select TE.Tipo as Estado_Aprobación from Cuestionario CU inner join Tipo_Estado TE on CU.Id_Estado_Aprobacion=TE.Id_Tipo_Estado where Id_Tipo_Cuestionario={id_tipo_cuestionario};"

    with connection.cursor() as cursor:
        cursor.execute(query)
        estadoAprobacion= cursor.fetchall()

    query=f"Select Id_Tipo_Estado,Tipo from Tipo_Estado;"

    with connection.cursor() as cursor:
        cursor.execute(query)
        tiposEstado= cursor.fetchall()



    context = {
        "tiposCuestionario": tiposCuestionario,
        "preguntas": preguntas,
        "id_tipo_cuestionario": id_tipo_cuestionario,
        "estadoEnvio":estadoEnvio,
        "estadoAprobacion":estadoAprobacion,
        "tiposEstado":tiposEstado
    }

    return render(request,'tablasAprobar.html',context)



def enviarAprobacion(request):
    id_tipo_estado=request.POST['id_tipo_estado']
    id_tipo_cuestionario=request.POST['id_tipo_cuestionario']
    query="Update Cuestionario set ID_Estado_Aprobacion=%s,Fecha_Revision=Current_Date,Hora_Revision=Current_Time(0) where Id_Tipo_Cuestionario=%s;"

    with connection.cursor() as cursor:
        cursor.execute(query,[id_tipo_estado,id_tipo_cuestionario])

    return redirect(f'/aprobar/{id_tipo_cuestionario}/')

