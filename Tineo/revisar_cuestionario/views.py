from django.shortcuts import render
from django.db import connection

# Create your views here.
def baseRevisar(request):
    with connection.cursor() as cursor:
        cursor.execute('SELECT ID_Tipo_Cuestionario, Tipo FROM Tipo_Cuestionario;')
        tiposCuestionario = cursor.fetchall()

    with connection.cursor() as cursor:
        cursor.execute('SELECT Id_Tipo_Respuesta,Tipo from Tipo_Respuesta;')
        tiposRespuesta = cursor.fetchall()

    query="Select Em.Id_Empleado,Em.Apellido_Empleado,Em.Nombre_Empleado, TR.Tipo as Calificacion from Empleado Em inner join Cuestionario_Empleado CE on Em.Id_Empleado=CE.Id_Empleado left join Reporte Re on Re.Id_Cuestionario_Empleado=Ce.Id_Cuestionario_Empleado left join Tipo_Respuesta TR on Re.Calificacion_Empleado=TR.Id_Tipo_Respuesta;"

    with connection.cursor() as cursor:
        cursor.execute(query)
        tablaEmpleados= cursor.fetchall()

    context = {
        "tiposCuestionario": tiposCuestionario,
        "tiposRespuesta": tiposRespuesta,
        "tablaEmpleados": tablaEmpleados
    }

    return render(request,'tablaEmpleados.html',context)


def revisarTipoCuestionario(request,id_tipo_cuestionario):
    with connection.cursor() as cursor:
        cursor.execute('SELECT ID_Tipo_Cuestionario, Tipo FROM Tipo_Cuestionario;')
        tiposCuestionario = cursor.fetchall()

    with connection.cursor() as cursor:
        cursor.execute('SELECT Id_Tipo_Respuesta,Tipo from Tipo_Respuesta;')
        tiposRespuesta = cursor.fetchall()

    query="Select Em.Id_Empleado,Em.Apellido_Empleado,Em.Nombre_Empleado, TR.Tipo as Calficacion from Empleado Em inner join Cuestionario_Empleado CE on Em.Id_Empleado=CE.Id_Empleado inner join Cuestionario CU on CE.ID_Cuestionario=Cu.ID_Cuestionario left join Reporte Re on Re.ID_Cuestionario_Empleado=Ce.ID_Cuestionario_Empleado left join Tipo_Respuesta TR on TR.ID_Tipo_Respuesta=Re.Calificacion_Empleado where Cu.ID_Tipo_Cuestionario=%s;"

    with connection.cursor() as cursor:
        cursor.execute(query,[id_tipo_cuestionario])
        tablaEmpleados= cursor.fetchall()
    
    context = {
        "tiposCuestionario": tiposCuestionario,
        "tiposRespuesta": tiposRespuesta,
        "tablaEmpleados": tablaEmpleados
    }

    return render(request,'tablaTipoCuestionario.html',context)


def revisarApellido(request):
    apellido= request.POST['apellido']

    with connection.cursor() as cursor:
        cursor.execute('SELECT ID_Tipo_Cuestionario, Tipo FROM Tipo_Cuestionario;')
        tiposCuestionario = cursor.fetchall()

    with connection.cursor() as cursor:
        cursor.execute('SELECT Id_Tipo_Respuesta,Tipo from Tipo_Respuesta;')
        tiposRespuesta = cursor.fetchall()

    query="Select Em.Id_Empleado,Em.Apellido_Empleado,Em.Nombre_Empleado, TR.Tipo as Calficacion from Empleado Em inner join Cuestionario_Empleado CE on Em.Id_Empleado=CE.Id_Empleado left join Reporte Re on Re.ID_Cuestionario_Empleado=Ce.ID_Cuestionario_Empleado left join Tipo_Respuesta TR on TR.ID_Tipo_Respuesta=Re.Calificacion_Empleado WHERE Em.Apellido_Empleado=%s;" 

    with connection.cursor() as cursor:
        cursor.execute(query,[apellido])
        tablaApellido= cursor.fetchall() 

    context = {        
        "tiposCuestionario": tiposCuestionario,
        "tiposRespuesta": tiposRespuesta,
        "tablaApellido": tablaApellido
    }


    return render(request,'tablaApellido.html',context)


def revisarCalificacion(request, id_tipo_calificacion):
    with connection.cursor() as cursor:
        cursor.execute('SELECT ID_Tipo_Cuestionario, Tipo FROM Tipo_Cuestionario;')
        tiposCuestionario = cursor.fetchall()

    with connection.cursor() as cursor:
        cursor.execute('SELECT Id_Tipo_Respuesta,Tipo from Tipo_Respuesta;')
        tiposRespuesta = cursor.fetchall()

    query="Select Em.Id_Empleado,Em.Apellido_Empleado,Em.Nombre_Empleado, TR.Tipo as Calficacion from Empleado Em inner join Cuestionario_Empleado CE on Em.Id_Empleado=CE.Id_Empleado left join Reporte Re on Re.Id_Cuestionario_Empleado=CE.Id_Cuestionario_Empleado left join Tipo_Respuesta TR on TR.ID_Tipo_Respuesta=Re.Calificacion_Empleado where calificacion_empleado=%s;" 

    with connection.cursor() as cursor:
        cursor.execute(query,[id_tipo_calificacion])
        tablaCalificacion= cursor.fetchall() 

    context = {        
        "tiposCuestionario": tiposCuestionario,
        "tiposRespuesta": tiposRespuesta,
        "tablaCalificacion": tablaCalificacion
    }


    return render(request,'tablaCalificacion.html',context)


def revisarCalificacionNULL(request):
    with connection.cursor() as cursor:
        cursor.execute('SELECT ID_Tipo_Cuestionario, Tipo FROM Tipo_Cuestionario;')
        tiposCuestionario = cursor.fetchall()

    with connection.cursor() as cursor:
        cursor.execute('SELECT Id_Tipo_Respuesta,Tipo from Tipo_Respuesta;')
        tiposRespuesta = cursor.fetchall()

    query="Select Em.Id_Empleado,Em.Apellido_Empleado,Em.Nombre_Empleado, TR.Tipo as Calficacion from Empleado Em inner join Cuestionario_Empleado CE on Em.Id_Empleado=CE.Id_Empleado left join Reporte Re on Re.Id_Cuestionario_Empleado=CE.Id_Cuestionario_Empleado left join Tipo_Respuesta TR on TR.ID_Tipo_Respuesta=Re.Calificacion_Empleado where calificacion_empleado IS NULL" 

    with connection.cursor() as cursor:
        cursor.execute(query)
        tablaCalificacion= cursor.fetchall() 

    context = {        
        "tiposCuestionario": tiposCuestionario,
        "tiposRespuesta": tiposRespuesta,
        "tablaCalificacion": tablaCalificacion
    }


    return render(request,'tablaCalificacion.html',context)








    



