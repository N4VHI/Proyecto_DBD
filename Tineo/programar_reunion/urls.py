from django.urls import path
from . import views

urlpatterns=[
    path('programarReunion/',views.baseProgramarReunion),
    path('botonProgramar/',views.botonProgramar)
]
