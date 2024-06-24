from django.shortcuts import render, redirect
from django.db import connection, IntegrityError
from django.http import HttpResponse
from datetime import datetime


def get_next_id(table_name, id_column):
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT COALESCE(MAX({id_column}), 0) + 1 FROM {table_name}")
        next_id = cursor.fetchone()[0]
    return next_id
def get_next_id2(table_name, id_column):
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT {id_column} FROM {table_name} ORDER BY {id_column} DESC LIMIT 1")
        last_id = cursor.fetchone()
        if last_id:
            last_id = last_id[0]
            next_id = str(int(last_id) + 1).zfill(len(last_id))
        else:
            next_id = '00000001'  # Comienza con '00000001' si no hay registros
    return next_id


def home(request):
    return render(request, 'home.html') 

def success_view(request):
    return render(request, 'success.html')

def listar_postulantes(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT ID_Cand, Nombre_Cand, Apell_Cand FROM Candidato")
        rows = cursor.fetchall()

    candidatos = [{'id_cand': row[0], 'nombre_cand': row[1], 'apell_cand': row[2]} for row in rows]
    
    return render(request, 'listar_postulantes.html', {'candidatos': candidatos})

def detalle_postulante(request, id_cand):
    with connection.cursor() as cursor:
        # Obtener los datos del candidato
        cursor.execute("SELECT * FROM Candidato WHERE ID_Cand = %s", [id_cand])
        row = cursor.fetchone()
        if not row:
            return HttpResponse("Candidato no encontrado", status=404)

        candidato = {
            'id_cand': row[0],
            'nombre_cand': row[1],
            'apell_cand': row[2],
            'fecha_nac_cand': row[3],
            'direccion_cand': row[4],
            'correo_cand': row[5],
            'num_telefono': row[6],
            'id_curriculum': row[7]
        }

        # Obtener los datos del curriculum
        cursor.execute("SELECT * FROM Curriculum WHERE ID_Curriculum = %s", [candidato['id_curriculum']])
        row = cursor.fetchone()
        if not row:
            return HttpResponse("Curriculum no encontrado", status=404)

        curriculum = {
            'id_curriculum': row[0],
            'grado_educacion': row[1],
            'archivo_pdf': row[4]
        }

        # Obtener las experiencias laborales
        cursor.execute("""
            SELECT EL.Nombre_Lugar, EL.Cargo_Ejercido, EL.Tiempo_Ejercido
            FROM Experiencia_Laboral EL
            JOIN CurriculumXExperiencia CE ON EL.ID_Experiencia = CE.id_experiencia
            WHERE CE.id_curriculum = %s
        """, [curriculum['id_curriculum']])
        experiencias = cursor.fetchall()

        # Obtener los certificados
        cursor.execute("""
            SELECT C.Curso_Certificado, C.Nivel_Certificado
            FROM Certificados C
            JOIN CurriculumXCertificado CC ON C.ID_Certificado = CC.id_certificado
            WHERE CC.id_curriculum = %s
        """, [curriculum['id_curriculum']])
        certificados = cursor.fetchall()

    return render(request, 'detalle_postulante.html', {
        'candidato': candidato,
        'curriculum': curriculum,
        'experiencias': experiencias,
        'certificados': certificados
    })


def registrar_postulante(request):
    if request.method == 'POST':
        nombre_cand = request.POST['nombre_cand']
        apell_cand = request.POST['apell_cand']
        fecha_nac_cand = request.POST['fecha_nac_cand']
        direccion_cand = request.POST['direccion_cand']
        correo_cand = request.POST['correo_cand']
        num_telefono = request.POST['num_telefono']
        grado_educacion = request.POST['grado_educacion']
        archivo_pdf = request.FILES['archivo_pdf']

        # Obtener listas de experiencias laborales
        nombre_lugar_list = request.POST.getlist('nombre_lugar')
        cargo_ejercido_list = request.POST.getlist('cargo_ejercido')
        tiempo_ejercido_list = request.POST.getlist('tiempo_ejercido')

        # Obtener listas de certificados
        curso_certificado_list = request.POST.getlist('curso_certificado')
        nivel_certificado_list = request.POST.getlist('nivel_certificado')

        with connection.cursor() as cursor:
            # Insertar experiencias laborales y obtener sus IDs
            experiencia_ids = []
            for nombre_lugar, cargo_ejercido, tiempo_ejercido in zip(nombre_lugar_list, cargo_ejercido_list, tiempo_ejercido_list):
                experiencia_id = get_next_id('Experiencia_Laboral', 'id_experiencia')
                cursor.execute("INSERT INTO Experiencia_Laboral (ID_Experiencia, Nombre_Lugar, Cargo_Ejercido, Tiempo_Ejercido) VALUES (%s, %s, %s, %s)",
                               [experiencia_id, nombre_lugar, cargo_ejercido, tiempo_ejercido])
                experiencia_ids.append(experiencia_id)

            # Insertar certificados y obtener sus IDs
            certificado_ids = []
            for curso_certificado, nivel_certificado in zip(curso_certificado_list, nivel_certificado_list):
                certificado_id = get_next_id('Certificados', 'id_certificado')
                cursor.execute("INSERT INTO Certificados (ID_Certificado, Curso_Certificado, Nivel_Certificado) VALUES (%s, %s, %s)",
                               [certificado_id, curso_certificado, nivel_certificado])
                certificado_ids.append(certificado_id)

            # Verificar si hay experiencias y certificados para el curriculum
            experiencia_id = experiencia_ids[0] if experiencia_ids else None
            certificado_id = certificado_ids[0] if certificado_ids else None

            # Insertar curriculum
            curriculum_id = get_next_id('Curriculum', 'id_curriculum')
            cursor.execute("INSERT INTO Curriculum (ID_Curriculum, Grado_Educacion, ID_Experiencia, ID_Certificado, archivo_pdf) VALUES (%s, %s, %s, %s, %s)", 
                           [curriculum_id, grado_educacion, experiencia_id, certificado_id, archivo_pdf.name])

            # Insertar las relaciones entre curriculum y experiencias laborales
            for experiencia_id in experiencia_ids:
                cursor.execute("INSERT INTO CurriculumXExperiencia (id_curriculum, id_experiencia) VALUES (%s, %s)", 
                               [curriculum_id, experiencia_id])

            # Insertar las relaciones entre curriculum y certificados
            for certificado_id in certificado_ids:
                cursor.execute("INSERT INTO CurriculumXCertificado (id_curriculum, id_certificado) VALUES (%s, %s)", 
                               [curriculum_id, certificado_id])

            # Insertar candidato
            candidato_id = get_next_id('Candidato', 'ID_Cand')
            cursor.execute("INSERT INTO Candidato (ID_Cand, Nombre_Cand, Apell_Cand, Fecha_Nac_Cand, Direccion_Cand, Correo_Cand, Num_Telefono, Id_Curriculum) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                           [candidato_id, nombre_cand, apell_cand, fecha_nac_cand, direccion_cand, correo_cand, num_telefono, curriculum_id])

        return redirect('success')
    else:
        return render(request, 'postulante_form.html')
    
def seleccionar_horario_puesto(request):
    if request.method == 'POST':
        id_solicitud = get_next_id2('Solicitud_Empleo', 'ID_Solicitud')
        id_vacante = request.POST.get('id_vacante')  # Asegúrate de que esta clave exista en el formulario
        est_solicitud = "Pendiente"
        horario_disponible = request.POST.get('horario_disponible')
        fecha_aplicacion = request.POST.get('fecha_aplicacion')
        id_cand = request.POST.get('id_cand')

        if not id_vacante:
            return render(request, 'seleccion_form.html', {
                'error': 'Debe seleccionar una vacante',
                'vacantes': get_vacantes(),
                'candidatos': get_candidatos()
            })

        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO Solicitud_Empleo (ID_Solicitud, ID_Vacante, Est_Solicitud, Horario_Disponible, Fecha_Aplicacion, ID_Cand) VALUES (%s, %s, %s, %s, %s, %s)",
                [id_solicitud, id_vacante, est_solicitud, horario_disponible, fecha_aplicacion, id_cand]
            )
        return redirect('success')
    else:
        vacantes = get_vacantes()
        candidatos = get_candidatos()
        return render(request, 'seleccion_form.html', {
            'vacantes': vacantes,
            'candidatos': candidatos
        })

def get_vacantes():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT DISTINCT v.ID_Vac, c.Nombre
            FROM Vacante v
            JOIN Cargo c ON v.ID_Cargo = c.ID_Cargo
            JOIN Solicitud_Empleo se ON v.ID_Vac = se.ID_Vacante
            WHERE se.Est_Solicitud = 'Pendiente' OR se.Est_Solicitud = 'En proceso'
        """)
        return cursor.fetchall()

def get_candidatos():
    with connection.cursor() as cursor:
        cursor.execute("SELECT ID_Cand, Nombre_Cand, Apell_Cand FROM Candidato")
        return cursor.fetchall()



def seleccionar_vacante(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT ID_Cargo, Nombre FROM Cargo")
        cargos = cursor.fetchall()
    
    return render(request, 'seleccionar_vacante.html', {'cargos': cargos})

def preseleccion_candidatos(request):
    if request.method == 'POST':
        cargo_id = request.POST.get('id_cargo', '')
        if 'preseleccionar' in request.POST:
            seleccionados = request.POST.getlist('seleccionados')
            if seleccionados:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "UPDATE Solicitud_Empleo SET Est_Solicitud = 'Preseleccionado' WHERE ID_Solicitud IN %s",
                        [tuple(seleccionados)]
                    )
                return redirect('success')
        else:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT se.ID_solicitud, c.ID_cand, c.Nombre_cand, c.Apell_cand, se.Horario_disponible, se.Est_solicitud
                    FROM Solicitud_Empleo se
                    JOIN Candidato c ON se.ID_cand = c.ID_cand
                    JOIN Vacante v ON se.ID_Vacante = v.ID_Vac
                    WHERE v.ID_Cargo = %s
                    AND (se.Est_solicitud = 'Pendiente' OR se.Est_solicitud = 'En proceso')
                """, [cargo_id])
                candidatos = cursor.fetchall()

            return render(request, 'preseleccion_list.html', {'candidatos': candidatos, 'cargo_id': cargo_id})
    else:
        return redirect('seleccionar_vacante')


    

def seleccion_final(request):
    if request.method == 'POST':
        seleccionados = request.POST.getlist('seleccionados')
        no_seleccionados = request.POST.getlist('no_seleccionados')
        
        if seleccionados or no_seleccionados:
            with connection.cursor() as cursor:
                if seleccionados:
                    cursor.execute(
                        "UPDATE Solicitud_Empleo SET Est_Solicitud = 'Seleccionado' WHERE ID_Solicitud IN %s",
                        [tuple(seleccionados)]
                    )
                if no_seleccionados:
                    cursor.execute(
                        "UPDATE Solicitud_Empleo SET Est_Solicitud = 'No Seleccionado' WHERE ID_Solicitud IN %s",
                        [tuple(no_seleccionados)]
                    )
            return redirect('success')
    else:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT se.ID_solicitud, c.ID_Cand, c.Nombre_Cand, c.Apell_Cand, d.Nombre_Departamento, ca.Nombre
                FROM Solicitud_Empleo se
                JOIN Candidato c ON se.ID_Cand = c.ID_Cand
                JOIN Vacante v ON se.ID_Vacante = v.ID_Vac
                JOIN Departamento d ON v.ID_Departamento = d.ID_Departamento
                JOIN Cargo ca ON v.ID_Cargo = ca.ID_Cargo
                WHERE se.Est_Solicitud = 'Preseleccionado'
            """)
            candidatos = cursor.fetchall()

        return render(request, 'seleccion_final.html', {'candidatos': candidatos})

def listado_seleccionados(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT se.ID_solicitud, c.Nombre_Cand, c.Apell_Cand, se.Fecha_Aplicacion, d.Nombre_Departamento, ca.Nombre
            FROM Solicitud_Empleo se
            JOIN Candidato c ON se.ID_Cand = c.ID_Cand
            JOIN Vacante v ON se.ID_Vacante = v.ID_Vac
            JOIN Departamento d ON v.ID_Departamento = d.ID_Departamento
            JOIN Cargo ca ON v.ID_Cargo = ca.ID_Cargo
            WHERE se.Est_Solicitud = 'Seleccionado'
            ORDER BY se.Fecha_Aplicacion DESC
        """)
        seleccionados = cursor.fetchall()

    return render(request, 'listado_seleccionados.html', {'seleccionados': seleccionados})


def crear_vacante(request):
    if request.method == 'POST':
        id_departamento = request.POST.get('id_departamento')
        id_cargo = request.POST.get('id_cargo')
        ubicacion = request.POST.get('ubicacion')
        beneficio = request.POST.get('beneficio')
        salario = request.POST.get('salario')
        horario = request.POST.get('horario')

        anos_exp = request.POST.get('anos_exp')
        conocimientos = request.POST.getlist('conocimientos')
        titulos = request.POST.getlist('titulos')

        try:
            with connection.cursor() as cursor:
                perfil_id = get_next_id('Perfil', 'ID_Perfil')
                cursor.execute(
                    "INSERT INTO Perfil (ID_Perfil, Anos_Exp) VALUES (%s, %s)",
                    [perfil_id, anos_exp]
                )

                for conocimiento in conocimientos:
                    cursor.execute(
                        "SELECT ID_Conocimiento FROM Conocimiento WHERE Nombre = %s",
                        [conocimiento]
                    )
                    conocimiento_id = cursor.fetchone()
                    if conocimiento_id is None:
                        conocimiento_id = get_next_id('Conocimiento', 'ID_Conocimiento')
                        cursor.execute(
                            "INSERT INTO Conocimiento (ID_Conocimiento, Nombre) VALUES (%s, %s)",
                            [conocimiento_id, conocimiento]
                        )
                    else:
                        conocimiento_id = conocimiento_id[0]
                    cursor.execute(
                        "INSERT INTO PerfilConocimiento (ID_Perfil, ID_Conocimiento) VALUES (%s, %s)",
                        [perfil_id, conocimiento_id]
                    )

                for titulo in titulos:
                    cursor.execute(
                        "SELECT ID_Titulo FROM Titulo WHERE Nombre = %s",
                        [titulo]
                    )
                    titulo_id = cursor.fetchone()
                    if titulo_id is None:
                        titulo_id = get_next_id('Titulo', 'ID_Titulo')
                        cursor.execute(
                            "INSERT INTO Titulo (ID_Titulo, Nombre) VALUES (%s, %s)",
                            [titulo_id, titulo]
                        )
                    else:
                        titulo_id = titulo_id[0]
                    cursor.execute(
                        "INSERT INTO PerfilTitulo (ID_Perfil, ID_Titulo) VALUES (%s, %s)",
                        [perfil_id, titulo_id]
                    )

                vacante_id = get_next_id2('Vacante', 'ID_Vac')
                cursor.execute(
                    "INSERT INTO Vacante (ID_Vac, ID_Departamento, ID_Cargo, ID_Perfil, Ubicacion, Beneficio, Salario, Horario) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                    [vacante_id, id_departamento, id_cargo, perfil_id, ubicacion, beneficio, salario, horario]
                )

            return redirect('success')
        except IntegrityError as e:
            return render(request, 'crear_vacante.html', {'error': str(e)})
    else:
        with connection.cursor() as cursor:
            cursor.execute("SELECT ID_Departamento, Nombre_Departamento FROM Departamento")
            departamentos = cursor.fetchall()
            cursor.execute("SELECT ID_Cargo, Nombre FROM Cargo")
            cargos = cursor.fetchall()
            cursor.execute("SELECT DISTINCT Ubicacion FROM Vacante")
            ubicaciones = cursor.fetchall()

        horarios = [
            "Turno Mañana: 9:00 am a 4:00 pm",
            "Turno Tarde: 12:00 pm a 8:00 pm"
        ]

        return render(request, 'crear_vacante.html', {
            'departamentos': departamentos,
            'cargos': cargos,
            'ubicaciones': ubicaciones,
            'horarios': horarios
        })


def listar_vacantes(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT v.ID_Vac, v.Ubicacion, v.Beneficio, v.Salario, v.Horario,
                   d.Nombre_Departamento, c.Nombre AS Cargo,
                   p.Anos_Exp, 
                   array_agg(DISTINCT co.Nombre) AS Conocimientos,
                   array_agg(DISTINCT t.Nombre) AS Titulos
            FROM Vacante v
            JOIN Departamento d ON v.ID_Departamento = d.ID_Departamento
            JOIN Cargo c ON v.ID_Cargo = c.ID_Cargo
            JOIN Perfil p ON v.ID_Perfil = p.ID_Perfil
            LEFT JOIN PerfilConocimiento pc ON p.ID_Perfil = pc.ID_Perfil
            LEFT JOIN Conocimiento co ON pc.ID_Conocimiento = co.ID_Conocimiento
            LEFT JOIN PerfilTitulo pt ON p.ID_Perfil = pt.ID_Perfil
            LEFT JOIN Titulo t ON pt.ID_Titulo = t.ID_Titulo
            GROUP BY v.ID_Vac, v.Ubicacion, v.Beneficio, v.Salario, v.Horario,
                     d.Nombre_Departamento, c.Nombre, p.Anos_Exp
            ORDER BY v.ID_Vac;
        """)
        vacantes = cursor.fetchall()

    return render(request, 'listar_vacantes.html', {'vacantes': vacantes})

def programar_entrevista(request):
    if request.method == 'POST':
        id_solicitud = request.POST.get('id_solicitud')
        fecha_eva = request.POST.get('fecha_eva')
        hora_entrevista = request.POST.get('hora_entrevista')
        id_empleado = request.POST.get('id_empleado')

        try:
            with connection.cursor() as cursor:
                entrevista_id = get_next_id('Entrevista', 'ID_Entrevista')
                evaluacion_id = get_next_id('Evaluacion', 'ID_Evaluacion')  # Asumiendo que la evaluación se crea al mismo tiempo
                cursor.execute(
                    "INSERT INTO Evaluacion (ID_Evaluacion, Competencias_Evaluadas, Result_Evaluacion, Duracion_Evaluacion, Estado_Evaluacion) VALUES (%s, %s, %s, %s, %s)",
                    [evaluacion_id, '', '', 0, 'Pendiente']
                )
                cursor.execute(
                    "INSERT INTO Entrevista (ID_Entrevista, Fecha_Eva, Hora_Entrevista, ID_Solicitud, ID_Empleado, ID_Evaluacion) VALUES (%s, %s, %s, %s, %s, %s)",
                    [entrevista_id, fecha_eva, hora_entrevista, id_solicitud, id_empleado, evaluacion_id]
                )
            return redirect('success')
        except IntegrityError as e:
            return render(request, 'programar_entrevista.html', {'error': str(e)})
    else:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT se.ID_Solicitud, c.Nombre_Cand, c.Apell_Cand
                FROM Solicitud_Empleo se
                JOIN Candidato c ON se.ID_Cand = c.ID_Cand
                WHERE se.Est_Solicitud = 'Preseleccionado'
            """)
            solicitudes = cursor.fetchall()
            cursor.execute("SELECT ID_Empleado, Nombre_Empleado FROM Empleado")
            empleados = cursor.fetchall()

        return render(request, 'programar_entrevista.html', {
            'solicitudes': solicitudes,
            'empleados': empleados
        })
def listar_entrevistas(request):
    estado = request.GET.get('estado', 'Pendiente')  # Default to 'Pendiente'
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT e.ID_Entrevista, e.Fecha_Eva, e.Hora_Entrevista, 
                   se.ID_Solicitud, c.Nombre_Cand, c.Apell_Cand,
                   em.Nombre_Empleado, ev.Estado_Evaluacion
            FROM Entrevista e
            JOIN Solicitud_Empleo se ON e.ID_Solicitud = se.ID_Solicitud
            JOIN Candidato c ON se.ID_Cand = c.ID_Cand
            JOIN Empleado em ON e.ID_Empleado = em.ID_Empleado
            JOIN Evaluacion ev ON e.ID_Evaluacion = ev.ID_Evaluacion
            WHERE ev.Estado_Evaluacion = %s
            ORDER BY e.Fecha_Eva, e.Hora_Entrevista
        """, [estado])
        entrevistas = cursor.fetchall()

    return render(request, 'listar_entrevistas.html', {'entrevistas': entrevistas, 'estado': estado})


from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.db import connection

from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.db import connection

def actualizar_evaluacion(request):
    if request.method == 'POST':
        id_entrevista = request.POST['id_entrevista']
        result_evaluacion = request.POST['result_evaluacion']
        duracion_evaluacion = request.POST['duracion_evaluacion']
        estado_evaluacion = request.POST['estado_evaluacion']
        competencias = request.POST.getlist('competencias[]')

        with connection.cursor() as cursor:
            # Actualizar evaluación
            cursor.execute("""
                UPDATE Evaluacion
                SET Result_Evaluacion = %s,
                    Duracion_Evaluacion = %s,
                    Estado_Evaluacion = %s
                WHERE ID_Evaluacion = (
                    SELECT ID_Evaluacion
                    FROM Entrevista
                    WHERE ID_Entrevista = %s
                )
            """, [result_evaluacion, duracion_evaluacion, estado_evaluacion, id_entrevista])

            # Obtener ID de la evaluación
            cursor.execute("""
                SELECT ID_Evaluacion
                FROM Entrevista
                WHERE ID_Entrevista = %s
            """, [id_entrevista])
            id_evaluacion = cursor.fetchone()[0]

            # Eliminar competencias actuales
            cursor.execute("""
                DELETE FROM EvaluacionXCompetencia
                WHERE ID_Evaluacion = %s
            """, [id_evaluacion])

            # Insertar nuevas competencias
            for competencia_id in competencias:
                cursor.execute("""
                    INSERT INTO EvaluacionXCompetencia (ID_Evaluacion, ID_Competencia)
                    VALUES (%s, %s)
                """, [id_evaluacion, competencia_id])

        return redirect('success')
    else:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT e.ID_Entrevista, c.Nombre_Cand, c.Apell_Cand, ev.Result_Evaluacion, ev.Duracion_Evaluacion, ev.Estado_Evaluacion
                FROM Entrevista e
                JOIN Solicitud_Empleo se ON e.ID_Solicitud = se.ID_Solicitud
                JOIN Candidato c ON se.ID_Cand = c.ID_Cand
                JOIN Evaluacion ev ON e.ID_Evaluacion = ev.ID_Evaluacion
            """)
            entrevistas = cursor.fetchall()
            
            cursor.execute("SELECT ID_Competencia, Nombre FROM Competencia")
            competencias = cursor.fetchall()

        return render(request, 'actualizar_evaluacion.html', {'entrevistas': entrevistas, 'competencias': competencias})

def listar_evaluaciones(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT ev.ID_Evaluacion, ev.Result_Evaluacion, ev.Duracion_Evaluacion, ev.Estado_Evaluacion,
                   COALESCE(STRING_AGG(c.Nombre, ', '), 'Ninguna') AS Competencias
            FROM Evaluacion ev
            LEFT JOIN EvaluacionXCompetencia ec ON ev.ID_Evaluacion = ec.ID_Evaluacion
            LEFT JOIN Competencia c ON ec.ID_Competencia = c.ID_Competencia
            GROUP BY ev.ID_Evaluacion, ev.Result_Evaluacion, ev.Duracion_Evaluacion, ev.Estado_Evaluacion
            ORDER BY ev.ID_Evaluacion
        """)
        evaluaciones = cursor.fetchall()

    return render(request, 'listar_evaluaciones.html', {'evaluaciones': evaluaciones})
