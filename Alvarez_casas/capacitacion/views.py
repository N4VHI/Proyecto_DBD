from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db import connection
from .models import Programa_Capacitador, Departamento

from django.urls import reverse

from datetime import datetime
from django.views.decorators.csrf import csrf_exempt

from capacitacion.models import Cargo

def tablacargo(request):
    cursor=connection.cursor()
    cursor.execute("select Cargo.Nombre, Cargo.Descripcion from Cargo")
    results=cursor.fetchall()
    return render(request,"signup.html",{'Cargo':results})
      
def departamentos_nombres(request):
    with connection.cursor() as cursor:
        cursor.execute('SELECT nombre_departamento FROM Departamento')
        nombre_deps=cursor.fetchall()
    return render(request,'registro_empleado.html',{"nombre_deps":nombre_deps})

def registrar_empleado(request):
    if request.method=='POST': 
        codigo_encargado = request.POST['codigo_encargado']
        motivo = request.POST['motivo']
        departamento_name = request.POST['ID_Departamento']
        numero_sesiones = request.POST['numero_sesiones']
        fecha_inicio= request.POST['fecha_inicio']
        fecha_fin = request.POST['fecha_fin']

        num=int(numero_sesiones)+1

        try:
            # Create a cursor object
            cursor = connection.cursor()

            # Get the ID of the department based on its name
            cursor.execute("SELECT id_departamento FROM Departamento WHERE nombre_departamento = %s", [departamento_name])
            departamento_result = cursor.fetchone()
        except:
            print("Error inserting data:")                

        query="INSERT INTO Programa_Capacitador (ID_Programa_C,Fecha_Inicio,Fecha_Fin,Motivo,ID_Departamento) VALUES ((SELECT ID_Programa_C FROM Programa_Capacitador ORDER BY ID_Programa_C DESC LIMIT 1)+1,%s, %s, %s, %s)"

        with connection.cursor() as cursor:
            cursor.execute(query,[fecha_inicio,fecha_fin,motivo,departamento_result])
        


        return redirect("registro_sesion/")
    

    return render(request,"registro_empleado.html")

def registrar_sesion(request):
        
    fecha_sesion=request.POST['fecha_sesion']
    hora_sesion=request.POST['hora_sesion']

    query="INSERT INTO Sesion(ID_Sesion,Estado,Fecha,Hora,ID_Programa_C) VALUES((SELECT ID_Sesion FROM Sesion ORDER BY ID_Sesion DESC LIMIT 1)+1,%s,%s,%s,(SELECT ID_Programa_C FROM Programa_Capacitador ORDER BY ID_Programa_C DESC LIMIT 1));"

    estado_default="Pendiente"

    with connection.cursor() as cursor:
        cursor.execute(query,[estado_default,fecha_sesion,hora_sesion]) 
    return render(request,"registro_sesion.html")

def matricular_empleado(request):
    codigo_programa=request.POST['codigo_programa']
    id_empleado=request.POST['cod_empleado']
    estado_default='Matriculado'

    query="INSERT INTO Lista_Matricula(ID_Programa_C,ID_Empleado,Estado_Matricula) VALUES(%s,%s,%s);"

    with connection.cursor() as cursor:
        cursor.execute(query,[codigo_programa,id_empleado,estado_default])
    return render(request,"matricular_empleado.html")

def helloworld1(request):
    return render(request,'signup.html')

def mostrarventana(request):
    return render(request,'registro_empleado.html')

def registro_sesion_ventana(request):
    return render(request,'registro_sesion.html')

def matricula_empleado_ventana(request):
    return render(request, "matricular_empleado.html")

def mostrar_matricula_ventana(request):
    return render(request,'lista_matricula_cap.html')

def muestra_capacitaciones(request):
    cursor=connection.cursor()
    cursor.execute("SELECT p.id_programa_c,	d.Nombre_Departamento,COUNT(DISTINCT s.ID_Sesion) AS Numero_Sesiones,p.Fecha_Inicio AS Fecha_Programa,COUNT(DISTINCT lm.ID_Empleado) AS Total_Empleados,p.Motivo FROM Programa_Capacitador p JOIN Departamento d ON p.ID_Departamento = d.ID_Departamento LEFT JOIN Sesion s ON p.ID_Programa_C = s.ID_Programa_C LEFT JOIN Lista_Matricula lm ON p.ID_Programa_C = lm.ID_Programa_C GROUP BY p.id_programa_c,d.Nombre_Departamento, p.Fecha_Inicio, p.Motivo ORDER BY p.id_programa_c;")
    results=cursor.fetchall()
    return render(request,'muestra_capacitaciones.html',{'solicitudes':results})

def ingresarIdPrograma(request):
    id_programa=request.POST['id_programa']
    return redirect(f'/mostrarMatricula/{id_programa}')

def mostrarMatricula(request,id_programa):
    query="SELECT CONCAT(Empleado.Nombre_Empleado, ' ', Empleado.Apellido_Empleado) AS Nombre_Completo,	Empleado.ID_Empleado,Lista_Matricula.Estado_Matricula FROM Empleado JOIN Lista_Matricula ON Empleado.ID_Empleado= Lista_Matricula.ID_Empleado JOIN Programa_Capacitador ON Lista_Matricula.ID_Programa_C = Programa_Capacitador.ID_Programa_C WHERE Programa_Capacitador.ID_Programa_C = %s;"

    with connection.cursor() as cursor:
        cursor.execute(query,[id_programa])
        result=cursor.fetchall()
    return render(request,"mostrarMatricula.html",{'matricula':result})

def ventana_asistencia(request):
    return render(request,"actualizar_asistencia.html")

def ingresarIdSesion(request):
    id_sesion=request.POST['id_sesion']
    fecha_sesion=request.POST['fecha_sesion']
    codigo_empleado=request.POST['codigo_empleado']
    asistencia=request.POST['asistencia']

    query="UPDATE Empleado_Sesion SET Asistencia = %s WHERE ID_Sesion IN (%s) AND ID_Empleado IN (%s);"

    with connection.cursor() as cursor:
        cursor.execute(query,[asistencia,id_sesion,codigo_empleado])

    return redirect(f'/mostrarAsistencia/{id_sesion}')

def mostrarAsistencia(request,id_sesion):
    query="SELECT CONCAT(Empleado.Nombre_Empleado, ' ', Empleado.Apellido_Empleado) AS Nombre_Completo, Empleado.ID_Empleado, Empleado_Sesion.Asistencia FROM Empleado INNER JOIN Empleado_Sesion ON Empleado.ID_Empleado=Empleado_Sesion.ID_Empleado INNER JOIN Sesion ON Empleado_Sesion.ID_Sesion=Sesion.ID_Sesion WHERE Sesion.ID_Sesion=%s;"

    with connection.cursor() as cursor:
        cursor.execute(query,[id_sesion])
        result=cursor.fetchall()
    
        
    return render(request,"actualizar_asistencia_2.html",{"Sesion":result})



