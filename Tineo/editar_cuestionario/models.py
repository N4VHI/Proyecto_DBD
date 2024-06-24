from django.db import models

# Create your models here.
class Cargo(models.Model):
    ID_Cargo = models.IntegerField(primary_key=True)
    Nombre = models.CharField(max_length=64, unique=True)
    Descripcion = models.CharField(max_length=264)

class Departamento(models.Model):
    ID_Departamento = models.IntegerField(primary_key=True)
    Nombre_Departamento = models.CharField(max_length=64, unique=True)

class Empleado(models.Model):
    ID_Empleado = models.IntegerField(primary_key=True)
    Nombre_Empleado = models.CharField(max_length=32)
    Apellido_Empleado = models.CharField(max_length=32)
    Telefono = models.CharField(max_length=15)
    Direccion = models.CharField(max_length=64)
    Correo = models.CharField(max_length=32, unique=True)
    Fecha_Nacimiento = models.DateField()
    Cant_Hijos = models.IntegerField(default=0)
    Estado_Civil = models.CharField(max_length=16)
    DNI = models.CharField(max_length=8)
    Fecha_Ingreso = models.DateField()
    ID_Departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE)
    ID_Cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE)

class Tipo_Estado(models.Model):
    ID_Tipo_Estado = models.IntegerField(primary_key=True)
    Tipo = models.CharField(max_length=12)


class Tipo_Cuestionario(models.Model):
    ID_Tipo_Cuestionario = models.IntegerField(primary_key=True)
    Tipo = models.CharField(max_length=12)

class Tipo_Respuesta(models.Model):
    ID_Tipo_Respuesta = models.IntegerField(primary_key=True)
    Tipo = models.CharField(max_length=12)

class Cuestionario(models.Model):
    ID_Cuestionario = models.IntegerField(primary_key=True)
    ID_Especialista_Relaciones_Laborales = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    ID_Tipo_Cuestionario = models.OneToOneField(Tipo_Cuestionario, on_delete=models.CASCADE)
    Fecha_Creacion = models.DateField()
    Hora_Creacion = models.TimeField()
    ID_Estado_Envio = models.ForeignKey(Tipo_Estado, on_delete=models.CASCADE)
    Fecha_Envio_Gerencia = models.DateField(null=True, blank=True)
    Hora_Envio_Gerencia = models.TimeField(null=True, blank=True)
    ID_Gerente = models.ForeignKey(Empleado, related_name='gerente', on_delete=models.CASCADE)
    ID_Estado_Aprobacion = models.ForeignKey(Tipo_Estado, related_name='estado_aprobacion', on_delete=models.CASCADE)
    Fecha_Revision = models.DateField(null=True, blank=True)
    Hora_Revision = models.TimeField(null=True, blank=True)

class Pregunta_Cuestionario(models.Model):
    ID_Pregunta = models.AutoField(primary_key=True)
    ID_Cuestionario = models.ForeignKey(Cuestionario, on_delete=models.CASCADE)
    Enunciado_Pregunta = models.CharField(max_length=256, unique=True)

class Cuestionario_Empleado(models.Model):
    ID_Cuestionario_Empleado = models.AutoField(primary_key=True)
    ID_Empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE, unique=True)
    ID_Cuestionario = models.ForeignKey(Cuestionario, on_delete=models.CASCADE)
    Fecha_Rellenado = models.DateField()
    Hora_Rellenado = models.TimeField()

class Respuesta_Cuestionario(models.Model):
    ID_Respuesta = models.AutoField(primary_key=True)
    ID_Pregunta = models.ForeignKey(Pregunta_Cuestionario, on_delete=models.CASCADE)
    ID_Cuestionario_Empleado = models.ForeignKey(Cuestionario_Empleado, on_delete=models.CASCADE)
    ID_Tipo_Respuesta = models.ForeignKey(Tipo_Respuesta, on_delete=models.CASCADE)

class Reporte(models.Model):
    ID_Reporte = models.AutoField(primary_key=True)
    ID_Cuestionario_Empleado = models.OneToOneField(Cuestionario_Empleado, on_delete=models.CASCADE, unique=True)
    Fecha_Ingreso_Empleado = models.DateField()
    Calificacion_Empleado = models.IntegerField()

class Retroalimentacion(models.Model):
    ID_Retroalimentacion = models.AutoField(primary_key=True)
    ID_Reporte = models.ForeignKey(Reporte, on_delete=models.CASCADE)
    Enunciado_Retroalimentacion = models.CharField(max_length=256)
    ID_Evaluador = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    Fecha_Retroalimentacion = models.DateField()
    Hora_Retroalimentacion = models.TimeField()

class Reunion(models.Model):
    ID_Reunion = models.AutoField(primary_key=True)
    ID_Organizador = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    Asunto_Reunion = models.CharField(max_length=256)
    Fecha_Reunion = models.DateField()
    Hora_Reunion = models.TimeField()