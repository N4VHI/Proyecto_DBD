from django import forms
from .models import Licencia, Departamento, Permiso

class LicenciaPermisoForm(forms.ModelForm):
    class Meta:
        model = Licencia
        fields = ['ID_Empleado', 'Motivo', 'Tipo', 'Fecha_inicio', 'Fecha_fin', 'ID_Supervisor']
        widgets = {
            'ID_Empleado': forms.TextInput(attrs={'maxlength': 8}),
            'Motivo': forms.Textarea(attrs={'rows': 2}),
            'Tipo': forms.Select(choices=Licencia.TIPOS_LICENCIA),
            'Fecha_inicio': forms.SelectDateWidget,
            'Fecha_fin': forms.SelectDateWidget,
            'ID_Supervisor': forms.TextInput(attrs={'maxlength': 8}),
        }
        labels = {
            'ID_Empleado': 'Código de Empleado',
            'Motivo': 'Motivo',
            'Fecha_inicio': 'Desde',
            'Fecha_fin': 'Hasta',
        }

class LicenciaApprovalForm(forms.ModelForm):
    class Meta:
        model = Licencia
        fields = ['Estado']

class ApproveRejectLicenciasForm(forms.Form):
    licencias = forms.ModelMultipleChoiceField(queryset=Licencia.objects.all(), widget=forms.CheckboxSelectMultiple)     

class ReporteAsistenciaForm(forms.Form):
    ID_Departamento = forms.ModelChoiceField(queryset=Departamento.objects.all(), label='Seleccione el área')
    fecha_desde = forms.DateField(widget=forms.SelectDateWidget, label='Desde')
    fecha_hasta = forms.DateField(widget=forms.SelectDateWidget, label='Hasta')

class PermisoForm(forms.ModelForm):
    class Meta:
        model = Permiso
        fields = ['tipo', 'motivo', 'duracion', 'id_empleado', 'id_supervisor']
        widgets = {
            'tipo': forms.Select(choices=Permiso.TIPOS_PERMISO),
            'motivo': forms.Textarea(attrs={'rows': 2}),
            'duracion': forms.TextInput(),
            'id_empleado': forms.NumberInput(),
            'id_supervisor': forms.NumberInput(),
        }