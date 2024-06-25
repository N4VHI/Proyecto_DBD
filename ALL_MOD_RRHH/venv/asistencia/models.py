from django.db import models

class Departamento(models.Model):
    ID_Departamento = models.IntegerField(primary_key=True)
    Nombre_Departamento = models.CharField(max_length=64)
    
    class Meta:
        db_table = 'Departamento'

    def __str__(self):
        return self.Nombre_Departamento

class Cargo(models.Model):
    ID_Cargo = models.IntegerField(primary_key=True)
    Nombre = models.CharField(max_length=64)
    Descripcion = models.CharField(max_length=264)

    class Meta:
        db_table = 'Cargo'

    def __str__(self):
        return self.Nombre

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

class Asistencia(models.Model):
    ID_Asistencia = models.IntegerField(primary_key=True)
    ID_Empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    Estado = models.CharField(max_length=1)
    Observacion = models.CharField(max_length=128)
    Fecha = models.DateField()
    Hora_entrada = models.TimeField()
    Hora_salida = models.TimeField()

    class Meta:
        db_table = 'Asistencia'

    def __str__(self):
        return f"Asistencia de {self.ID_Empleado} el {self.Fecha}"

class Licencia(models.Model):
    TIPOS_LICENCIA = [
        ('Mudanza', 'Mudanza'),
        ('Matrimonio', 'Matrimonio'),
        ('Nacimiento de un familiar', 'Nacimiento de un familiar'),
        ('Fallecimiento de un familiar', 'Fallecimiento de un familiar'),
        ('Accidente de un familiar', 'Accidente de un familiar'),
        ('Enfermedad grave de un familiar', 'Enfermedad grave de un familiar'),
        ('Deberes inexcusables', 'Deberes inexcusables'),
        ('Exámenes prenatales', 'Exámenes prenatales'),
        ('Funciones sindicales', 'Funciones sindicales'),
        ('Hijos prematuros', 'Hijos prematuros'),
        ('Formación', 'Formación'),
        ('Despido objetivo', 'Despido objetivo'),
    ]
    
    ID_Licencia = models.AutoField(primary_key=True)
    ID_Empleado = models.IntegerField()
    ID_Supervisor = models.IntegerField()
    Motivo = models.CharField(max_length=128)
    Fecha_inicio = models.DateField()
    Fecha_fin = models.DateField()
    Tipo = models.CharField(max_length=64, choices=TIPOS_LICENCIA)
    Estado = models.CharField(max_length=64, default='Pendiente')

    def __str__(self):
        return f"Licencia {self.ID_Licencia} - {self.Tipo}"

class Permiso(models.Model):
    TIPOS_PERMISO = [
        ('Mudanza', 'Mudanza'),
        ('Matrimonio', 'Matrimonio'),
        ('Nacimiento de un familiar', 'Nacimiento de un familiar'),
        ('Fallecimiento de un familiar', 'Fallecimiento de un familiar'),
        ('Accidente de un familiar', 'Accidente de un familiar'),
        ('Enfermedad grave de un familiar', 'Enfermedad grave de un familiar'),
        ('Deberes inexcusables', 'Deberes inexcusables'),
        ('Exámenes prenatales', 'Exámenes prenatales'),
        ('Funciones sindicales', 'Funciones sindicales'),
        ('Hijos prematuros', 'Hijos prematuros'),
        ('Formación', 'Formación'),
        ('Despido objetivo', 'Despido objetivo'),
    ]

    id_permiso = models.AutoField(primary_key=True)
    tipo = models.CharField(max_length=64, choices=TIPOS_PERMISO)
    motivo = models.CharField(max_length=128)
    duracion = models.CharField(max_length=64)
    estado = models.CharField(max_length=64, default='Pendiente')
    id_empleado = models.IntegerField()
    id_supervisor = models.IntegerField()

    class Meta:
        db_table = 'Permiso'

    def __str__(self):
        return f"Permiso {self.ID_Permiso} de {self.ID_Empleado.Nombre_Empleado}"

class Supervisor(models.Model):
    ID_Supervisor = models.AutoField(primary_key=True)
    ID_Empleado = models.OneToOneField(Empleado, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Supervisor'

    def __str__(self):
        return f"Supervisor: {self.ID_Empleado.Nombre_Empleado} {self.ID_Empleado.Apellido_Empleado}"