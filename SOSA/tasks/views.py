# tasks/views.py

from django.shortcuts import render, redirect
from .forms import CandidatoForm, SolicitudEmpleoForm, PerfilForm, EntrevistaForm, EvaluacionForm
from .models import SolicitudEmpleo, Candidato, Perfil, Entrevista, Evaluacion
def home(request):
    return render(request, 'home.html') 

def registrar_postulante(request):
    if request.method == 'POST':
        form = CandidatoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success')  # Ajustar el nombre de la vista de éxito según tu configuración
    else:
        form = CandidatoForm()
    return render(request, 'postulante_form.html', {'form': form})

def seleccionar_horario_puesto(request):
    if request.method == 'POST':
        form = SolicitudEmpleoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success')  # Ajustar el nombre de la vista de éxito según tu configuración
    else:
        form = SolicitudEmpleoForm()
    return render(request, 'seleccion_form.html', {'form': form})

def preseleccion_candidatos(request):
    # Aquí ajustamos la consulta para utilizar los nuevos modelos y relaciones
    vacante_id = '00200001'  # Ajusta este valor según tu lógica real
    candidatos = Candidato.objects.filter(solicitudempleo__id_vacante=vacante_id, solicitudempleo__est_solicitud__in=['Pendiente', 'En proceso'])
    return render(request, 'preseleccion_list.html', {'candidatos': candidatos})

def seleccion_final(request):
    if request.method == 'POST':
        ids_solicitudes = request.POST.getlist('ids_solicitudes')
        SolicitudEmpleo.objects.filter(id_solicitud__in=ids_solicitudes).update(est_solicitud='Seleccionado')
        return redirect('success')  # Ajustar el nombre de la vista de éxito según tu configuración
    return render(request, 'seleccion_final.html')

def crear_perfil(request):
    if request.method == 'POST':
        form = PerfilForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success')  # Ajustar el nombre de la vista de éxito según tu configuración
    else:
        form = PerfilForm()
    return render(request, 'perfil_form.html', {'form': form})

def programar_entrevista(request):
    if request.method == 'POST':
        form = EntrevistaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success')  # Ajustar el nombre de la vista de éxito según tu configuración
    else:
        form = EntrevistaForm()
    return render(request, 'entrevista_form.html', {'form': form})

def actualizar_evaluacion(request):
    if request.method == 'POST':
        form = EvaluacionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success')  # Ajustar el nombre de la vista de éxito según tu configuración
    else:
        form = EvaluacionForm()
    return render(request, 'evaluacion_form.html', {'form': form})
