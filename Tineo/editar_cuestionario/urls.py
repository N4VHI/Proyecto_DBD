from django.urls import path
from . import views

urlpatterns=[
    path('editar/',views.baseEditar),
    path('editar/<int:id_tipo_cuestionario>/',views.mostrarPreguntas),
    path('agregarPregunta/',views.agregarPregunta),
    path('borrarPregunta/<int:id_pregunta>/',views.borrarPregunta),
    path('enviarGerencia/',views.enviarGerencia),
]
