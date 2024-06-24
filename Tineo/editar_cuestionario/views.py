from django.shortcuts import render,redirect
from django.db import connection

# Create your views here.
def baseEditar(request):
    with connection.cursor() as cursor:
        cursor.execute('SELECT ID_Tipo_Cuestionario, Tipo FROM Tipo_Cuestionario;')
        tiposCuestionario = cursor.fetchall()
    return render(request,'baseEditar.html',{"tiposCuestionario":tiposCuestionario})


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


    context = {
        "tiposCuestionario": tiposCuestionario,
        "preguntas": preguntas,
        "id_tipo_cuestionario": id_tipo_cuestionario,
        "estadoEnvio":estadoEnvio,
        "estadoAprobacion":estadoAprobacion
    }

    return render(request,'tablaPreguntas.html',context)


def agregarPregunta(request):
    id_tipo_cuestionario=request.POST['id_tipo_cuestionario']
    enunciado_pregunta=request.POST['enunciado_pregunta']

    query = "INSERT INTO Pregunta_Cuestionario(ID_Pregunta, ID_Cuestionario, Enunciado_Pregunta) VALUES (CASE WHEN (SELECT MAX(ID_Pregunta) FROM Pregunta_Cuestionario) IS NULL THEN 1 ELSE (SELECT (MAX(ID_Pregunta)) FROM Pregunta_Cuestionario) + 1 END, %s, %s);"
    
    with connection.cursor() as cursor:
            cursor.execute(query, [id_tipo_cuestionario, enunciado_pregunta])
            
    return redirect(f'/editar/{id_tipo_cuestionario}/')


def borrarPregunta(request,id_pregunta):
    id_tipo_cuestionario=request.POST['id_tipo_cuestionario']
    query = "DELETE FROM Pregunta_Cuestionario WHERE ID_Pregunta = %s;"
    
    with connection.cursor() as cursor:
            cursor.execute(query, [id_pregunta])
            
    return redirect(f'/editar/{id_tipo_cuestionario}/')


def enviarGerencia(request):
    id_tipo_cuestionario=request.POST['id_tipo_cuestionario']

    query=f"Update Cuestionario set ID_Estado_Envio=1, Fecha_Envio_Gerencia=Current_Date, Hora_Envio_Gerencia=Current_Time(0), ID_Estado_Aprobacion=5 where Id_Tipo_Cuestionario={id_tipo_cuestionario};"

    with connection.cursor() as cursor:
        cursor.execute(query)

    return redirect(f'/editar/{id_tipo_cuestionario}/') 