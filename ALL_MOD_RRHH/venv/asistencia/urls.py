from django.contrib import admin
from django.urls import path
from . import views 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('MenuPrincipal', views.MenuPrincipal, name='MenuPrincipal'),
    path('', views.MostrarFormulario),
    path('InsertarAsistencia/', views.Insert),
    path('empleados_por_departamento/<int:departamento_id>/', views.empleados_por_departamento, name='empleados_por_departamento'),
    path('SolicitarLicencia/', views.solicitar_licencia, name='solicitar_licencia'),
    path('SolicitarPermiso/', views.solicitar_permiso, name='solicitar_permiso'),
    path('AceptarRechazarSolicitudes/', views.aprobar_rechazar_solicitudes, name='aprobar_rechazar_solicitudes'),
    path('GenerarReporteAsistencia/', views.generar_reporte_asistencia, name='Generar_reporte_asistencia'),
    path('MostrarReporte/<int:departamento_id>/<str:fecha_inicio>/<str:fecha_fin>/', views.mostrar_reporte, name='mostrar_reporte'),
    path('aprobar_rechazar_permisos/', views.aprobar_rechazar_permisos, name='aprobar_rechazar_permisos'),
]