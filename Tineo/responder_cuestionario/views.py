from django.shortcuts import render, redirect
from django.db import connection

# Create your views here.
def baseResponder(request):
    with connection.cursor() as cursor:
        cursor.execute('SELECT ID_Tipo_Cuestionario, Tipo FROM Tipo_Cuestionario;')
        tiposCuestionario = cursor.fetchall()
    return render(request,'baseResponder.html',{"tiposCuestionario":tiposCuestionario})

def mostrarPreguntas(request,id_tipo_cuestionario):
    with connection.cursor() as cursor:
        cursor.execute('SELECT ID_Tipo_Cuestionario, Tipo FROM Tipo_Cuestionario;')
        tiposCuestionario = cursor.fetchall()

    query=f"SELECT PC.ID_Pregunta, PC.Enunciado_Pregunta FROM Pregunta_Cuestionario PC INNER JOIN Cuestionario C ON PC.ID_Cuestionario = C.ID_Cuestionario WHERE C.ID_Tipo_Cuestionario = {id_tipo_cuestionario};"

    with connection.cursor() as cursor:
        cursor.execute(query)
        preguntas= cursor.fetchall()

    query=f"SELECT Id_Tipo_Respuesta,Tipo from Tipo_Respuesta;"

    with connection.cursor() as cursor:
        cursor.execute(query)
        tiposRespuesta= cursor.fetchall()

    context = {
        "tiposCuestionario": tiposCuestionario,
        "preguntas": preguntas,
        "id_tipo_cuestionario": id_tipo_cuestionario,
        "tiposRespuesta": tiposRespuesta,
    }

    return render(request,'tablaResponder.html',context)

def enviarRespuestas(request):
    id_empleado = request.POST['id_empleado']
    id_tipo_cuestionario = request.POST['id_tipo_cuestionario']
        
    query="INSERT INTO Cuestionario_Empleado(ID_Cuestionario_Empleado,ID_Empleado,ID_Cuestionario,Fecha_Rellenado,Hora_Rellenado) VALUES (CASE WHEN (SELECT MAX(ID_Cuestionario_Empleado) FROM Cuestionario_Empleado) IS NULL THEN 1 ELSE (SELECT MAX(ID_Cuestionario_Empleado) FROM Cuestionario_Empleado) + 1 END,%s,(Select Id_Cuestionario from Cuestionario where Id_tipo_Cuestionario=%s),Current_Date,Current_Time(0));"
 
    with connection.cursor() as cursor:
        cursor.execute(query, [id_empleado, id_tipo_cuestionario])            

    query= "INSERT INTO Respuesta_Cuestionario(ID_Respuesta,ID_Pregunta,ID_Cuestionario_Empleado,ID_Tipo_Respuesta) VALUES (CASE WHEN (SELECT MAX(ID_Respuesta) FROM Respuesta_Cuestionario) IS NULL THEN 1 ELSE (SELECT MAX(ID_Respuesta) FROM Respuesta_Cuestionario) + 1 END, %s,(Select ID_Cuestionario_Empleado FROM Cuestionario_Empleado where ID_Empleado=%s),%s);"

        
    with connection.cursor() as cursor:
        for key, value in request.POST.items():
            if key.startswith('respuesta_'):
                id_pregunta = key.split('_')[1]
                id_tipo_respuesta = value
                cursor.execute(query, [id_pregunta, id_empleado, id_tipo_respuesta])
        
    return redirect(f'/responder/')
