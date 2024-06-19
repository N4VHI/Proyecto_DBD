# tasks/forms.py

from django import forms
from .models import Candidato, SolicitudEmpleo, Perfil, Entrevista, Evaluacion, Empleado

class CandidatoForm(forms.ModelForm):
    class Meta:
        model = Candidato
        fields = '__all__'

class SolicitudEmpleoForm(forms.ModelForm):
    class Meta:
        model = SolicitudEmpleo
        fields = '__all__'

class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = '__all__'

class EntrevistaForm(forms.ModelForm):
    class Meta:
        model = Entrevista
        fields = '__all__'

class EvaluacionForm(forms.ModelForm):
    class Meta:
        model = Evaluacion
        fields = '__all__'

class EmpleadoForm(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = '__all__'
