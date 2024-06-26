
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.db import connection
from .forms import LicenciaPermisoForm
from django.utils.dateparse import parse_date
from django.urls import reverse

def MostrarFormulario(request):
    if 'show_form' in request.GET:
        with connection.cursor() as cursor:
            cursor.execute("SELECT ID_Departamento, Nombre_Departamento FROM Departamento")
            departamentos = cursor.fetchall()
        return render(request, 'Index.html', {'departamentos': departamentos})
    else:
        return redirect('/MenuPrincipal')

def empleados_por_departamento(request, departamento_id):
    query = "SELECT ID_Empleado, Nombre_Empleado, Apellido_Empleado FROM Empleado WHERE ID_Departamento = %s"
    with connection.cursor() as cursor:
        cursor.execute(query, [departamento_id])
        empleados = cursor.fetchall()
    return JsonResponse(list(empleados), safe=False)


def Insert(request):
    if request.method == "POST":
        Estado = request.POST['Estado']
        Observacion = request.POST['Observacion']
        Fecha = request.POST['Fecha']
        Hora_entrada = request.POST['Hora_entrada']
        Hora_salida = request.POST['Hora_salida']
        ID_Empleado = request.POST['ID_Empleado']
        query = "INSERT INTO Asistencia (ID_Asistencia, Estado, Observacion, Fecha, Hora_entrada, Hora_salida, ID_Empleado) VALUES ((SELECT COALESCE(MAX(ID_Asistencia), 0) + 1 FROM Asistencia), %s, %s, %s, %s, %s, %s)"
        with connection.cursor() as cursor:
            cursor.execute(query, [Estado, Observacion, Fecha, Hora_entrada, Hora_salida, ID_Empleado])
        messages.success(request, 'Asistencia insertada')
        return redirect('/MenuPrincipal/')
    return render(request, 'Index.html')

def solicitar_licencia(request):
    if request.method == 'POST':
        form = LicenciaPermisoForm(request.POST, request.FILES)
        if form.is_valid():
            id_empleado = form.cleaned_data['ID_Empleado']
            motivo = form.cleaned_data['Motivo']
            fecha_inicio = form.cleaned_data['Fecha_inicio']
            fecha_fin = form.cleaned_data['Fecha_fin']
            estado = 'Pendiente'
            tipo = 'Licencia'
            id_supervisor = 1  # Este valor deberá ser dinámico según tu lógica

            query = """
            INSERT INTO Licencia (ID_Licencia, Tipo, Estado, Fecha_inicio, Fecha_fin, ID_Empleado, ID_Supervisor)
            VALUES ((SELECT COALESCE(MAX(ID_Licencia), 0) + 1 FROM Licencia), %s, %s, %s, %s, %s, %s)
            """
            with connection.cursor() as cursor:
                cursor.execute(query, [tipo, estado, fecha_inicio, fecha_fin, id_empleado, id_supervisor])

            messages.success(request, 'La solicitud de licencia ha sido enviada correctamente.')
            return redirect('/')
        else:
            messages.error(request, 'Hubo un error en la solicitud.')
    else:
        form = LicenciaPermisoForm()
    return render(request, 'solicitar_licencia.html', {'form': form})

def aprobar_rechazar_solicitudes(request):
    if request.method == 'POST':
        licencias = request.POST.getlist('licencias')
        accion = request.POST.get('accion')

        if accion == 'aprobar':
            estado_nuevo = 'Aprobado'
        elif accion == 'rechazar':
            estado_nuevo = 'Rechazado'
        else:
            messages.error(request, 'Acción no válida.')
            return redirect('aprobar_rechazar_solicitudes')

        query = '''
        UPDATE Licencia
        SET Estado = %s
        WHERE ID_Licencia = %s
        '''
        
        with connection.cursor() as cursor:
            for licencia_id in licencias:
                cursor.execute(query, [estado_nuevo, licencia_id])

        messages.success(request, 'Licencias actualizadas correctamente.')
        return redirect('aprobar_rechazar_solicitudes')
    else:
        query = '''
        SELECT l.ID_Licencia, l.Tipo, l.Estado, l.Fecha_inicio, l.Fecha_fin, e.Nombre_Empleado, e.Apellido_Empleado
        FROM Licencia l
        JOIN Empleado e ON l.ID_Empleado = e.ID_Empleado
        WHERE l.Estado = 'Pendiente'
        '''
        
        with connection.cursor() as cursor:
            cursor.execute(query)
            licencias = cursor.fetchall()
        
        if licencias:
            return render(request, 'aprobar_rechazar_solicitudes.html', {'licencias': licencias})
        else:
            return render(request, 'aprobar_rechazar_solicitudes.html')
        
def MenuPrincipal(request):
    return render(request, 'Menu.html')

def generar_reporte_asistencia(request):
    if request.method == 'POST':
        departamento_id = request.POST.get('departamento')
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_fin = request.POST.get('fecha_fin')
        
        if departamento_id and fecha_inicio and fecha_fin:
            return redirect(reverse('mostrar_reporte', args=[departamento_id, fecha_inicio, fecha_fin]))
    
    with connection.cursor() as cursor:
        cursor.execute("SELECT ID_Departamento, Nombre_Departamento FROM Departamento")
        departamentos = cursor.fetchall()
    return render(request, 'Generar_reporte_asistencia.html', {'departamentos': departamentos})

def mostrar_reporte(request, departamento_id, fecha_inicio, fecha_fin):
    fecha_inicio = parse_date(fecha_inicio)
    fecha_fin = parse_date(fecha_fin)
    
    query = '''
    SELECT a.ID_Asistencia, a.Estado, a.Observacion, a.Fecha, a.Hora_entrada, a.Hora_salida, e.Nombre_Empleado, e.Apellido_Empleado
    FROM Asistencia a
    JOIN Empleado e ON a.ID_Empleado = e.ID_Empleado
    WHERE e.ID_Departamento = %s AND a.Fecha BETWEEN %s AND %s
    '''
    
    with connection.cursor() as cursor:
        cursor.execute(query, [departamento_id, fecha_inicio, fecha_fin])
        asistencias = cursor.fetchall()
    
    if asistencias:
        return render(request, 'Mostrar_reporte.html', {'asistencias': asistencias})
    else:
        messages.info(request, 'No se han registrado asistencias entre esas fechas.')
        return render(request, 'Mostrar_reporte.html')


def solicitar_permiso(request):
    if request.method == 'POST':
        tipo = request.POST.get('tipo')
        motivo = request.POST.get('motivo')
        duracion = request.POST.get('duracion')
        id_empleado = request.POST.get('id_empleado')
        id_supervisor = request.POST.get('id_supervisor')
        estado = 'Pendiente' 
        query = """
        INSERT INTO Permiso (ID_Permiso, Tipo, Motivo, Duracion, Estado, ID_Empleado, ID_Supervisor)
        VALUES ((SELECT COALESCE(MAX(ID_Permiso), 0) + 1 FROM Permiso), %s, %s, %s, %s, %s, %s)
        """
        
        with connection.cursor() as cursor:
            cursor.execute(query, [tipo, motivo, duracion, estado, id_empleado, id_supervisor])
        
        messages.success(request, 'Solicitud de permiso enviada correctamente.')
        return redirect('MenuPrincipal')
    return render(request, 'solicitar_permiso.html')

def solicitar_licencia(request):
    if request.method == 'POST':
        form = LicenciaPermisoForm(request.POST, request.FILES)
        if form.is_valid():
            id_empleado = form.cleaned_data['ID_Empleado']
            motivo = form.cleaned_data['Motivo']
            fecha_inicio = form.cleaned_data['Fecha_inicio']
            fecha_fin = form.cleaned_data['Fecha_fin']
            id_supervisor = form.cleaned_data['ID_Supervisor']
            tipo = form.cleaned_data['Tipo']
            estado = 'Pendiente'
            

            query = """
            INSERT INTO Licencia (ID_Licencia, Tipo, Estado, Fecha_inicio, Fecha_fin, ID_Empleado, ID_Supervisor)
            VALUES ((SELECT COALESCE(MAX(ID_Licencia), 0) + 1 FROM Licencia), %s, %s, %s, %s, %s, %s)
            """
            with connection.cursor() as cursor:
                cursor.execute(query, [tipo, estado, fecha_inicio, fecha_fin, id_empleado, id_supervisor])

            messages.success(request, 'La solicitud de licencia ha sido enviada correctamente.')
            return redirect('/')
        else:
            messages.error(request, 'Hubo un error en la solicitud.')
    else:
        form = LicenciaPermisoForm()
    return render(request, 'solicitar_licencia.html', {'form': form})

def aprobar_rechazar_permisos(request):
    if request.method == 'POST':
        permisos = request.POST.getlist('permisos')
        accion = request.POST.get('accion')

        if accion == 'aprobar':
            estado_nuevo = 'Aprobado'
        elif accion == 'rechazar':
            estado_nuevo = 'Rechazado'
        else:
            messages.error(request, 'Acción no válida.')
            return redirect('aprobar_rechazar_permisos')

        query = '''
        UPDATE Permiso
        SET Estado = %s
        WHERE ID_Permiso = %s
        '''
        
        with connection.cursor() as cursor:
            for permiso_id in permisos:
                cursor.execute(query, [estado_nuevo, permiso_id])

        messages.success(request, 'Permisos actualizados correctamente.')
        return redirect('aprobar_rechazar_permisos')
    else:
        query = '''
        SELECT p.ID_Permiso, p.Tipo, p.Estado, p.duracion, e.Nombre_Empleado, e.Apellido_Empleado
        FROM Permiso p
        JOIN Empleado e ON p.ID_Empleado = e.ID_Empleado
        WHERE p.Estado = 'Pendiente'
        '''
        
        with connection.cursor() as cursor:
            cursor.execute(query)
            permisos = cursor.fetchall()
        
        if permisos:
            return render(request, 'aprobar_rechazar_permisos.html', {'permisos': permisos})
        else:
            return render(request, 'aprobar_rechazar_permisos.html')
