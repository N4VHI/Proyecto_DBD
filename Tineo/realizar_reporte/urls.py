from django.urls import path
from . import views

urlpatterns=[
    path('reporte/<id_empleado>/',views.reporteBase),
    path('confirmarReporte/',views.confirmarReporte)
]




