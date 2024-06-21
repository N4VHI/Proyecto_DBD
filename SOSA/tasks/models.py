# tasks/models.py

from django.db import models

class Cargo(models.Model):
    ID_Cargo = models.IntegerField(primary_key=True)
    Nombre = models.CharField(max_length=64, null=False, blank=False)
    Descripcion = models.CharField(max_length=264, null=False, blank=False)

class Departamento(models.Model):
    ID_Departamento = models.IntegerField(primary_key=True)
    Nombre_Departamento = models.CharField(max_length=64, null=False, blank=False)

class Empleado(models.Model):
    ID_Empleado = models.IntegerField(primary_key=True)
    Nombre_Empleado = models.CharField(max_length=32, null=False, blank=False) 
    Apellido_Empleado = models.CharField(max_length=32, null=False, blank=False)
    Telefono = models.CharField(max_length=15, null=False, blank=False) 
    Direccion = models.CharField(max_length=64, null=False, blank=False)
    Correo = models.CharField(max_length=64, null=False, blank=False, unique=True) 
    Fecha_Nacimiento = models.DateField(null=False, blank=False)
    Cant_Hijos = models.IntegerField(default=0) 
    Estado_Civil = models.CharField(max_length=15, null=False, blank=False) 
    DNI = models.CharField(max_length=8, null=False, blank=False)
    Fecha_Ingreso = models.DateField(null=False, blank=False) 
    ID_Departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE)
    ID_Cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE)

class Candidato(models.Model):
    id_cand = models.AutoField(primary_key=True)
    nombre_cand = models.CharField(max_length=255)
    apell_cand = models.CharField(max_length=255)
    fecha_nac_cand = models.DateField()
    direccion_cand = models.CharField(max_length=255)
    correo_cand = models.EmailField()
    num_telefono = models.CharField(max_length=15)
    id_curriculum = models.ForeignKey('Curriculum', on_delete=models.CASCADE)

class Curriculum(models.Model):
    id_curriculum = models.AutoField(primary_key=True)
    grado_educacion = models.CharField(max_length=255)
    id_experiencia = models.ForeignKey('ExperienciaLaboral', on_delete=models.CASCADE)
    id_certificado = models.ForeignKey('Certificados', on_delete=models.CASCADE)

class Certificados(models.Model):
    id_certificado = models.AutoField(primary_key=True)
    curso_certificado = models.CharField(max_length=255)
    nivel_certificado = models.CharField(max_length=255)

class ExperienciaLaboral(models.Model):
    id_experiencia = models.AutoField(primary_key=True)
    nombre_lugar = models.CharField(max_length=255)
    cargo_ejercido = models.CharField(max_length=255)
    tiempo_ejercido = models.CharField(max_length=50)

class SolicitudEmpleo(models.Model):
    id_solicitud = models.CharField(max_length=8, primary_key=True)
    id_vacante = models.CharField(max_length=8)
    est_solicitud = models.CharField(max_length=255)
    horario_disponible = models.CharField(max_length=255)
    fecha_aplicacion = models.DateField()
    id_cand = models.ForeignKey(Candidato, on_delete=models.CASCADE)

class Perfil(models.Model):
    id_perfil = models.AutoField(primary_key=True)
    conocimiento_req = models.CharField(max_length=255)
    anos_exp = models.IntegerField()
    titulo_requerido = models.CharField(max_length=255)

class Vacante(models.Model):
    id_vac = models.CharField(max_length=8, primary_key=True)
    id_departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE)
    id_cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE)
    id_perfil = models.ForeignKey(Perfil, on_delete=models.CASCADE)
    ubicacion = models.CharField(max_length=255)
    beneficio = models.CharField(max_length=255)
    salario = models.DecimalField(max_digits=8, decimal_places=2)
    horario = models.CharField(max_length=255)

class Entrevista(models.Model):
    id_entrevista = models.AutoField(primary_key=True)
    fecha_eva = models.DateField()
    hora_entrevista = models.TimeField()
    id_solicitud = models.ForeignKey(SolicitudEmpleo, on_delete=models.CASCADE)
    id_evaluacion = models.ForeignKey('Evaluacion', on_delete=models.CASCADE)
    id_empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)

class Evaluacion(models.Model):
    id_evaluacion = models.AutoField(primary_key=True)
    competencias_evaluadas = models.CharField(max_length=255)
    result_evaluacion = models.CharField(max_length=255)
    duracion_evaluacion = models.IntegerField()
    estado_evaluacion = models.CharField(max_length=255)
