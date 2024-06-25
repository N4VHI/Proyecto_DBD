from django.shortcuts import render, redirect
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



def mostrarReuniones(request):
    query="SELECT Asunto_Reunion, Fecha_Reunion, Hora_Reunion FROM Reunion;"

    with connection.cursor() as cursor:
        cursor.execute(query)
        reuniones=cursor.fetchall()
    
    context={
        "reuniones":reuniones
    }

    return render(request,'reunionesBase.html',context)

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

def mostrarMenu(request):
    return render(request,'menuBase.html')

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
    
