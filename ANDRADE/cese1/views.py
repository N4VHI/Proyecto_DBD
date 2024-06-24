from django.shortcuts import render, redirect
from django.db import connection

def login(request):
    if request.method == "POST":
        codigo_empleado = request.POST.get("codigo_empleado")
        password = request.POST.get("password")

        query_verificar_usuario = """
            SELECT id_empleado 
            FROM empleado 
            WHERE id_empleado = %s AND contrasena = %s
        """
        with connection.cursor() as cursor:
            cursor.execute(query_verificar_usuario, [codigo_empleado, password])
            resultado = cursor.fetchone()

        query_verificar_estado = """
            SELECT id_cese
            FROM empleado AS E
            INNER JOIN cese AS C ON C.id_empleado = E.id_empleado
            WHERE C.id_empleado = %s AND E.Estado_laboral='cesado'
        """
        with connection.cursor() as cursor:
            cursor.execute(query_verificar_estado, [codigo_empleado])
            estado = cursor.fetchone()

        query_verificar_cargo = """
            SELECT id_empleado, id_cargo 
            FROM empleado 
            WHERE id_cargo BETWEEN 1 AND 4
        """
        with connection.cursor() as cursor:
            cursor.execute(query_verificar_cargo)
            cargo = cursor.fetchone()

        if resultado:
            if estado:
                request.session['id_cese'] = estado[0]
                return redirect('cese5')
            
            elif cargo:
                request.session['id_supervisor'] = resultado[0]
                return redirect('seleccion')

    return render(request, 'login.html')

def seleccion(request):
    if request.method == "POST":
        if 'action' in request.POST and request.POST['action'] == 'cesar_empleado':
            # Obtener el próximo id_cese disponible
            query_nuevo_id_cese = """
                SELECT COALESCE(MAX(id_cese), 0) + 1 
                FROM cese
            """
            with connection.cursor() as cursor:
                cursor.execute(query_nuevo_id_cese)
                id_cese = cursor.fetchone()[0]

            # Guardar id_cese en la sesión
            request.session['id_cese'] = id_cese

            # Redirigir a la vista cese1 para comenzar el proceso de cese
            return redirect('cese1')

    return render(request, 'seleccion.html')

def cese1(request):
    id_supervisor = request.session.get('id_supervisor')
    if not id_supervisor:
        return redirect('login')

    id_cese = request.session.get('id_cese')
    if not id_cese:
        return redirect('seleccion')

    resultados_empleados = []
    id_empleado = None

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "buscar":
            apellido_entrante = request.POST.get("buscador_apellido")
            query_buscar_empleado = """
                SELECT E.DNI, E.nombre_empleado AS NOMBRE, E.apellido_empleado AS APELLIDO, D.nombre_departamento, E.id_empleado 
                FROM empleado AS E 
                INNER JOIN departamento AS D ON E.id_departamento = D.id_departamento 
                WHERE E.apellido_empleado LIKE %s
            """
            with connection.cursor() as cursor:
                cursor.execute(query_buscar_empleado, [f'%{apellido_entrante}%'])
                resultados_empleados = cursor.fetchall()

        elif action == "seleccionar_empleado":
            id_empleado = request.POST.get("seleccionar_empleado")
            request.session['id_empleado'] = id_empleado

        elif action == "enviar_cese":
            id_empleado = request.session.get('id_empleado')
            if not id_empleado:
                return redirect('cese1')

            tipo_cese = request.POST.get("tipo_cese")
            motivo_cese = request.POST.get("motivo_cese")
            fecha_cese = request.POST.get("fecha_cese")
            cant_deuda = request.POST.get("cant_deuda", None)  # Deuda opcional

            query_nuevo_id_cese = """
                SELECT COALESCE(MAX(id_cese), 0) + 1 
                FROM cese
            """
            with connection.cursor() as cursor:
                cursor.execute(query_nuevo_id_cese)
                comparar = cursor.fetchone()[0]

            if(comparar == id_cese):

                if motivo_cese:
                    query_insertar_cese = """
                        INSERT INTO cese (id_cese, tipo_cese, motivo_cese, fecha_inicio_cese, id_supervisor, id_empleado) 
                        VALUES (%s, %s, %s, %s, %s, %s);

                        UPDATE empleado
                        SET Estado_laboral = 'cesado'
                        WHERE id_empleado = %s;
                    """
                    with connection.cursor() as cursor:
                        cursor.execute(query_insertar_cese, [id_cese, tipo_cese, motivo_cese, fecha_cese, id_supervisor, id_empleado, id_empleado])
                else:
                    query_insertar_cese = """
                        INSERT INTO cese (id_cese, tipo_cese, motivo_cese, fecha_inicio_cese, id_supervisor, id_empleado) 
                        VALUES (%s, %s, Null, %s, %s, %s);

                        UPDATE empleado
                        SET Estado_laboral = 'cesado'
                        WHERE id_empleado = %s;
                    """
                    with connection.cursor() as cursor:
                        cursor.execute(query_insertar_cese, [id_cese, tipo_cese, fecha_cese, id_supervisor, id_empleado, id_empleado])

                if cant_deuda:
                    query_insertar_deuda = """
                        INSERT INTO beneficios_cese (id_beneficios, id_tipo, monto, id_cese)
                        VALUES (
                            (SELECT COALESCE(MAX(id_beneficios), 0) + 1 FROM beneficios_cese), 
                            5, 
                            -1 * %s, 
                            %s
                        );
                    """
                    with connection.cursor() as cursor:
                        cursor.execute(query_insertar_deuda, [cant_deuda, id_cese])  
            
            else:
                
                query_correccion = """
                    UPDATE empleado
                    SET Estado_laboral = 'activo'
                    WHERE id_empleado = (SELECT id_empleado FROM cese WHERE id_cese=%s);
                """
                with connection.cursor() as cursor:
                    cursor.execute(query_correccion,id_cese)

                if motivo_cese:
                    query_insertar_cese = """
                        UPDATE cese 
                        SET 
                            tipo_cese = %s, 
                            motivo_cese = %s, 
                            fecha_inicio_cese = %s, 
                            id_supervisor = %s, 
                            id_empleado = %s
                        WHERE id_cese = %s;

                        UPDATE empleado
                        SET Estado_laboral = 'cesado'
                        WHERE id_empleado = %s;
                    """
                    with connection.cursor() as cursor:
                        cursor.execute(query_insertar_cese, [tipo_cese, motivo_cese, fecha_cese, id_supervisor, id_empleado, id_cese, id_empleado])
                else:
                    query_insertar_cese = """
                        UPDATE cese 
                        SET 
                            tipo_cese = %s, 
                            motivo_cese = null, 
                            fecha_inicio_cese = %s, 
                            id_supervisor = %s, 
                            id_empleado = %s
                        WHERE id_cese = %s;

                        UPDATE empleado
                        SET Estado_laboral = 'cesado'
                        WHERE id_empleado = %s;
                    """
                    with connection.cursor() as cursor:
                        cursor.execute(query_insertar_cese, [tipo_cese, fecha_cese, id_supervisor, id_empleado, id_cese, id_empleado])

                if cant_deuda:
                    query_insertar_deuda = """
                        UPDATE beneficios_cese 
                        SET
                            monto = -1 * %s
                        WHERE id_Cese =%s and id_tipo=5
                    """
                    with connection.cursor() as cursor:
                        cursor.execute(query_insertar_deuda, [cant_deuda, id_cese]) 

            return redirect('cese2', id_cese=id_cese)

    return render(request, 'cese1.html', {'empleados': resultados_empleados})

def cese2(request, id_cese):
    query_revisar_empleado = """
        SELECT id_empleado, nombre, departamento, cargo, fecha_cese, tipo_cese, motivo, id_supervisor 
        FROM detalles_cese
        WHERE C.id_cese = %s
    """
    with connection.cursor() as cursor:
        cursor.execute(query_revisar_empleado, [id_cese])
        resultados_revisar = cursor.fetchall()

    query_montos = """
        SELECT
            SUM(B.monto)
        FROM cese AS C
        INNER JOIN beneficios_cese AS B ON C.id_cese = B.id_cese
        WHERE C.id_cese = %s
    """
    with connection.cursor() as cursor:
        cursor.execute(query_montos, [id_cese])
        resultados_monto = cursor.fetchall()

    return render(request, 'cese2.html', {'revisar': resultados_revisar, 'beneficios': resultados_monto})

def cese3(request):

    id_cese = request.session.get('id_cese')
    if not id_cese:
        return redirect('seleccion')

    if request.method == "POST":
        action = request.POST.get("action")

        if action == 'preguntas_predeterminadas':
            # Primero, insertar el cuestionario si no existe
            query_existe_cuestionario = """
                SELECT id_cuestionario FROM cuestionario_salida WHERE id_cese = %s
            """
            with connection.cursor() as cursor:
                cursor.execute(query_existe_cuestionario, [id_cese])
                existe_cuestionario = cursor.fetchone()

            if not existe_cuestionario:
                query_insertar_cuestionario = """
                    WITH last_cuestionario AS (
                        SELECT COALESCE(MAX(id_cuestionario), 0) + 1 AS id_cuestionario FROM cuestionario_salida
                    )
                    INSERT INTO cuestionario_salida (id_cuestionario, id_cese)
                    VALUES (
                        (SELECT id_cuestionario FROM last_cuestionario),
                        %s
                    )
                    RETURNING id_cuestionario
                """
                with connection.cursor() as cursor:
                    cursor.execute(query_insertar_cuestionario, [id_cese])
                    id_cuestionario = cursor.fetchone()[0]
                    request.session['id_cuestionario'] = id_cuestionario
            else:
                id_cuestionario = existe_cuestionario[0]
                request.session['id_cuestionario'] = id_cuestionario

            # Insertar las preguntas predeterminadas
            query_insertar_preguntas = """
                WITH last_id AS (
                    SELECT COALESCE(MAX(id_pregunta), 0) AS id_pregunta FROM pregunta_salida
                )
                INSERT INTO pregunta_salida (id_pregunta, pregunta_salida, id_cuestionario)
                VALUES
                    ((SELECT id_pregunta FROM last_id) + 1, '¿Cómo describirías tu experiencia en tu empresa?', %s),
                    ((SELECT id_pregunta FROM last_id) + 2, '¿Qué mejorarías en la empresa?', %s),
                    ((SELECT id_pregunta FROM last_id) + 3, '¿Qué no te gusta de tu empresa?', %s)
            """
            with connection.cursor() as cursor:
                cursor.execute(query_insertar_preguntas, [id_cuestionario, id_cuestionario, id_cuestionario])

        elif action == "enviar_pregunta":
            pregunta_nueva = request.POST.get("pregunta_nueva")

            query_existe_cuestionario = """
                SELECT id_cuestionario FROM cuestionario_salida WHERE id_cese = %s
            """
            with connection.cursor() as cursor:
                cursor.execute(query_existe_cuestionario, [id_cese])
                existe_cuestionario = cursor.fetchone()

            if existe_cuestionario:
                id_cuestionario = existe_cuestionario[0]
                request.session['id_cuestionario'] = id_cuestionario

                query_insertar_nueva_pregunta = """
                    WITH last_id AS (
                        SELECT COALESCE(MAX(id_pregunta), 0) AS id_pregunta FROM pregunta_salida
                    )
                    INSERT INTO pregunta_salida (id_pregunta, pregunta_salida, id_cuestionario)
                    VALUES (
                        (SELECT id_pregunta FROM last_id) + 1,
                        %s,
                        %s
                    )
                """
                with connection.cursor() as cursor:
                    cursor.execute(query_insertar_nueva_pregunta, [pregunta_nueva, id_cuestionario])

            else:
                query_insertar_cuestionario = """
                    WITH last_cuestionario AS (
                        SELECT COALESCE(MAX(id_cuestionario), 0) + 1 AS id_cuestionario FROM cuestionario_salida
                    )
                    INSERT INTO cuestionario_salida (id_cuestionario, id_cese)
                    VALUES (
                        (SELECT id_cuestionario FROM last_cuestionario),
                        %s
                    )
                    RETURNING id_cuestionario
                """
                with connection.cursor() as cursor:
                    cursor.execute(query_insertar_cuestionario, [id_cese])
                    id_cuestionario = cursor.fetchone()[0]
                    request.session['id_cuestionario'] = id_cuestionario

                query_insertar_nueva_pregunta = """
                    WITH last_id AS (
                        SELECT COALESCE(MAX(id_pregunta), 0) + 1 AS id_pregunta FROM pregunta_salida
                    )
                    INSERT INTO pregunta_salida (id_pregunta, pregunta_salida, id_cuestionario)
                    VALUES (
                        (SELECT id_pregunta FROM last_id),
                        %s,
                        %s
                    )
                """
                with connection.cursor() as cursor:
                    cursor.execute(query_insertar_nueva_pregunta, [pregunta_nueva, id_cuestionario])

    return render(request, 'cese3.html')

def cese4(request):
    return render(request, 'cese4.html')

def cese5(request):
    return render(request, 'cese5.html')

def cese6(request):
    id_cuestionario = request.session.get('id_cuestionario')
    if not id_cuestionario:
        return redirect('cese3')

    if request.method == "POST" and request.POST.get("action") == "confirmar":
        query_buscar_pregunta = """
            SELECT id_pregunta 
            FROM pregunta_salida
            WHERE id_cuestionario=%s
        """
        with connection.cursor() as cursor:
            cursor.execute(query_buscar_pregunta, [id_cuestionario])
            preguntas_ids = cursor.fetchall()
        
        respuestas = {}
        for index, pregunta in enumerate(preguntas_ids, start=1):
            respuesta = request.POST.get(f'respuesta_{index}')
            if respuesta:
                respuestas[pregunta[0]] = respuesta

        # Insertar respuestas en la base de datos
        query_insertar_respuesta = """
            INSERT INTO respuesta_salida (id_respuesta, id_pregunta, respuesta_salida)
            VALUES ((SELECT COALESCE(MAX(id_respuesta), 0) + 1 FROM respuesta_salida), %s, %s)
        """
        with connection.cursor() as cursor:
            for id_pregunta, respuesta in respuestas.items():
                cursor.execute(query_insertar_respuesta, [id_pregunta, respuesta])
        
        return redirect('cese7')  # Redirigir a una página de confirmación

    query_buscar_pregunta = """
        SELECT pregunta_salida 
        FROM pregunta_salida
        WHERE id_cuestionario=%s
    """
    with connection.cursor() as cursor:
        cursor.execute(query_buscar_pregunta, [id_cuestionario])
        resultados_preguntas = cursor.fetchall()

    return render(request, 'cese6.html', {'preguntas': resultados_preguntas})

def cese7(request):
    return render(request, 'cese7.html')