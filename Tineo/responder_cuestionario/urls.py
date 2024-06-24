from django.urls import path
from . import views

urlpatterns=[
    path('responder/',views.baseResponder),
    path('responder/<id_tipo_cuestionario>/',views.mostrarPreguntas),
    path('enviarRespuestas/',views.enviarRespuestas)
]
