from django.db import models


# Create your models here.
class Cargo(models.Model):
    ID_Cargo=models.IntegerField(primary_key=True)
    Nombre=models.CharField(max_length=64,null=False,blank=False)
    Descripcion=models.CharField(max_length=264,null=False,blank=False)

class Departamento(models.Model):
    ID_Departamento=models.IntegerField(primary_key=True)
    Nombre_Departamento=models.CharField(max_length=64,null=False,blank=False)

class Empleado(models.Model):

    ID_Empleado=models.IntegerField(primary_key=True)
    Nombre_Empleado=models.CharField(max_length=32,null=False,blank=False) 
    Apellido_Empleado =models.CharField(max_length=32,null=False,blank=False)
    Telefono=models.CharField(max_length=15,null=False,blank=False) 
    Direccion=models.CharField(max_length=64,null=False,blank=False)
    Correo=models.CharField(max_length=15,null=False,blank=False, unique=True) 
    Fecha_Nacimiento=models.DateField(null=False,blank=False)
    Cant_Hijos=models.IntegerField(default=0) 
    Estado_Civil=models.CharField(max_length=15,null=False,blank=False) 
    DNI=models.CharField(max_length=8,null=False,blank=False)
    Fecha_Ingreso=models.DateField(null=False,blank=False) 
    ID_Departamento=models.ForeignKey(Departamento,on_delete=models.CASCADE,)
    ID_Cargo=models.ForeignKey(Cargo,on_delete=models.CASCADE,)
	

class Programa_Capacitador(models.Model):
    id_programa_c=models.IntegerField(primary_key=True)
    fecha_inicio=models.DateField(null=False,blank=False)
    fecha_fin=models.DateField(null=False,blank=False)
    motivo=models.CharField(max_length=256,null=False,blank=False)
    ID_Departamento=models.ForeignKey(Departamento, on_delete=models.CASCADE)



class Lista_Matricula(models.Model):
    id_programa_c=models.ForeignKey(Programa_Capacitador, on_delete=models.CASCADE)
    ID_Empleado=models.ForeignKey(Empleado, on_delete=models.CASCADE)
    estado_matricula=models.CharField(max_length=256,null=False,blank=False)

class Sesion(models.Model):
    id_sesion=models.IntegerField(primary_key=True)
    estado=models.CharField(max_length=64,null=False,blank=False,default="Programado")
    fecha=models.DateField(null=False,blank=False)
    hora=models.TimeField(null=False,blank=False)
    id_programa_c=models.ForeignKey(Programa_Capacitador, on_delete=models.CASCADE)

class Empleado_Sesion(models.Model):
    id_sesion=models.ForeignKey(Sesion, on_delete=models.CASCADE)
    ID_Empleado=models.ForeignKey(Empleado, on_delete=models.CASCADE)
    asistencia=models.CharField(max_length=64,null=False,blank=False)

class Evaluacion_Capacitacion(models.Model):
    id_evaluacion=models.IntegerField(primary_key=True)
    duracion_evaluacion=models.IntegerField(null=False,blank=False)
    hora=models.TimeField(null=False,blank=False)
    instructor=models.ForeignKey(Empleado, on_delete=models.CASCADE)

class Evaluacion_Sesion(models.Model):
    id_evaluacion=models.ForeignKey(Evaluacion_Capacitacion, on_delete=models.CASCADE)
    id_sesion=models.ForeignKey(Sesion,on_delete=models.CASCADE)
    resultado=models.CharField(max_length=64,null=False,blank=False)

class Evaluacion_Empleado(models.Model):
    id_evaluacion=models.ForeignKey(Evaluacion_Capacitacion, on_delete=models.CASCADE)
    id_empleado=models.ForeignKey(Empleado,on_delete=models.CASCADE)
    resultado=models.CharField(max_length=64, null=False, blank=False)


