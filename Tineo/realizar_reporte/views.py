from django.shortcuts import render,redirect
from django.db import connection

# Create your views here.
def reporteBase(request,id_empleado):


    with connection.cursor() as cursor:
        cursor.execute('SELECT Id_Tipo_Respuesta,Tipo from Tipo_Respuesta;')
        tiposCalificacion= cursor.fetchall()

    query="SELECT DISTINCT Em.id_empleado, Em.apellido_empleado, Em.nombre_empleado, Ce.ID_Cuestionario_Empleado, TC.Tipo FROM Empleado Em INNER JOIN Cuestionario_Empleado CE ON Em.id_empleado = CE.id_empleado INNER JOIN Cuestionario Cu ON CE.id_cuestionario = Cu.id_cuestionario INNER JOIN Tipo_Cuestionario TC ON Cu.id_tipo_cuestionario = TC.id_tipo_cuestionario where em.id_empleado=%s;"

    with connection.cursor() as cursor:
        cursor.execute(query,[id_empleado])
        datosEmpleado= cursor.fetchall()

    query="SELECT ROW_NUMBER() OVER (ORDER BY PC.ID_Pregunta) AS Nº, PC.Enunciado_Pregunta, TR.Tipo AS Respuesta FROM Empleado Em INNER JOIN Cuestionario_Empleado CE ON Em.id_empleado = CE.id_empleado INNER JOIN Respuesta_Cuestionario RC ON CE.ID_Cuestionario_Empleado = RC.ID_Cuestionario_Empleado INNER JOIN Pregunta_Cuestionario PC ON RC.ID_Pregunta = PC.ID_Pregunta INNER JOIN Tipo_Respuesta TR ON RC.ID_Tipo_Respuesta = TR.ID_Tipo_Respuesta WHERE Em.id_empleado = %s;"

    with connection.cursor() as cursor:
        cursor.execute(query,[id_empleado])
        tablaRespuestas= cursor.fetchall()
 
    context = {
        "tiposCalificacion": tiposCalificacion,
        "datosEmpleado": datosEmpleado,
        "tablaRespuestas": tablaRespuestas,
        'id_empleado':id_empleado
    }

    return render(request,'reportebase.html',context)



def confirmarReporte(request):
    id_empleado = request.POST['id_empleado']
    id_evaluador = request.POST['id_evaluador']
    retroalimentacion = request.POST['retroalimentacion']
    calificacion=request.POST['calificacion']

    query="INSERT INTO Reporte (ID_Reporte, ID_Cuestionario_Empleado, Fecha_Ingreso_Empleado, Calificacion_Empleado) VALUES (CASE WHEN (SELECT MAX(ID_Reporte) FROM Reporte) IS NULL THEN 1 ELSE (SELECT MAX(ID_Reporte) FROM Reporte) + 1 END,(Select ID_Cuestionario_Empleado from Cuestionario_Empleado where Id_Empleado=%s),(Select Fecha_Ingreso from Empleado where ID_empleado=%s),%s);"

    with connection.cursor() as cursor:
        cursor.execute(query,[id_empleado,id_empleado,calificacion])
    
    query="INSERT INTO Retroalimentacion (ID_Retroalimentacion, ID_Reporte, Enunciado_Retroalimentacion, ID_Evaluador, Fecha_Retroalimentacion, Hora_Retroalimentacion) VALUES (CASE WHEN (SELECT MAX(ID_Retroalimentacion) FROM Retroalimentacion) IS NULL THEN 1 ELSE (SELECT MAX(ID_Retroalimentacion) FROM Retroalimentacion) + 1 END, (SELECT Re.ID_Reporte FROM Reporte Re INNER JOIN Cuestionario_Empleado CE ON Re.ID_Cuestionario_Empleado = CE.ID_Cuestionario_Empleado WHERE CE.ID_Empleado = %s LIMIT 1),%s, %s, CURRENT_DATE, CURRENT_TIME(0));"

    with connection.cursor() as cursor:
        cursor.execute(query,[id_empleado,retroalimentacion, id_evaluador])   

    return redirect('/revisar/')