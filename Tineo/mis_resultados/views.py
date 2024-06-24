from django.shortcuts import render,redirect
from django.db import connection

# Create your views here.
def baseMisResultados(request):
    return render(request,'baseMisResultados.html')

def ingresarID(request):
    id_empleado=request.POST['id_empleado']
    return redirect(f'/misResultadosID/{id_empleado}/')

def ingresarDNI(request):
    dni=request.POST['dni']
    return redirect(f'/misResultadosDNI/{dni}/')

def ingresarApellido(request):
    apellido=request.POST['apellido']
    return redirect(f'/misResultadosApellido/{apellido}/')


def mostrarResultadosID(request,id_empleado):
    query="SELECT Em.ID_Empleado, Em.Nombre_Empleado, Em.Apellido_Empleado, Re.Fecha_Ingreso_Empleado, TR.Tipo as Calificacion, Ret.Enunciado_Retroalimentacion FROM Empleado Em INNER JOIN Cuestionario_Empleado CE ON Em.ID_Empleado = CE.ID_Empleado INNER JOIN Reporte Re ON CE.ID_Cuestionario_Empleado = Re.ID_Cuestionario_Empleado INNER JOIN Retroalimentacion Ret ON Re.ID_Reporte = Ret.ID_Reporte INNER JOIN Tipo_Respuesta TR ON TR.ID_Tipo_Respuesta=Re.Calificacion_Empleado WHERE Em.ID_Empleado = %s;"

    with connection.cursor() as cursor:
        cursor.execute(query,[id_empleado])
        resultados=cursor.fetchall()

    context={
        "resultados":resultados
    }

    return render(request,'mostrarResultados.html',context)

def mostrarResultadosDNI(request,dni):
    query="SELECT Em.ID_Empleado, Em.Nombre_Empleado, Em.Apellido_Empleado, Re.Fecha_Ingreso_Empleado, TR.Tipo as Calificacion, Ret.Enunciado_Retroalimentacion FROM Empleado Em INNER JOIN Cuestionario_Empleado CE ON Em.ID_Empleado = CE.ID_Empleado INNER JOIN Reporte Re ON CE.ID_Cuestionario_Empleado = Re.ID_Cuestionario_Empleado INNER JOIN Retroalimentacion Ret ON Re.ID_Reporte = Ret.ID_Reporte INNER JOIN Tipo_Respuesta TR ON TR.ID_Tipo_Respuesta=Re.Calificacion_Empleado WHERE Em.dni = %s;"

    with connection.cursor() as cursor:
        cursor.execute(query,[dni])
        resultados=cursor.fetchall()

    context={
        "resultados":resultados
    }

    return render(request,'mostrarResultados.html',context)


def mostrarTablaApellidos(request,apellido):
    query="Select Em.Apellido_Empleado, Nombre_Empleado, Em.ID_Empleado from Empleado Em inner join Cuestionario_Empleado Cu on Cu.Id_Empleado=Em.Id_Empleado inner join Reporte Re on Re.Id_Cuestionario_Empleado=Cu.Id_Cuestionario_Empleado where Em.apellido_empleado=%s;"

    with connection.cursor() as cursor:
        cursor.execute(query,[apellido])
        empleados=cursor.fetchall()

    context={
        "empleados": empleados
    }

    return render(request,'mostrarTablaApellido.html',context)
