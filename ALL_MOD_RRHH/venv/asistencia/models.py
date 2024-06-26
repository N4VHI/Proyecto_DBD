from django.db import models

class Departamento(models.Model):
    ID_Departamento = models.IntegerField(primary_key=True)
    Nombre_Departamento = models.CharField(max_length=64)
    
    class Meta:
        db_table = 'Departamento'

    def __str__(self):
        return self.Nombre_Departamento
    
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
    ID_Departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE, null=True, blank=True)
    ID_Cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table = 'Empleado'

    def __str__(self):
        return f"{self.Nombre_Empleado} {self.Apellido_Empleado}"
