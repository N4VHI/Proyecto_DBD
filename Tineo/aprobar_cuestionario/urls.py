from django.urls import path
from . import views

urlpatterns=[
    path('aprobar/',views.baseAprobar),
    path('aprobar/<id_tipo_cuestionario>/',views.mostrarPreguntas),
    path('enviarAprobacion/',views.enviarAprobacion)
]
