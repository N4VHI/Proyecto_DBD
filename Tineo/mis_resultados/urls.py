from django.urls import path
from . import views

urlpatterns=[
    path('misResultados/',views.baseMisResultados),
    path('ingresarID/',views.ingresarID),
    path('ingresarDNI/',views.ingresarDNI),
    path('ingresarApellido/',views.ingresarApellido),
    path('misResultadosDNI/<dni>/',views.mostrarResultadosDNI),
    path('misResultadosID/<id_empleado>/',views.mostrarResultadosID),
    path('misResultadosApellido/<apellido>/',views.mostrarTablaApellidos)
]
