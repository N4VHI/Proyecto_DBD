"""
URL configuration for modulo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from tasks import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('registrar/', views.registrar_postulante, name='registrar_postulante'),
    path('success/', views.success_view, name='success'),
    path('postulantes/', views.listar_postulantes, name='listar_postulantes'),
    path('postulantes/<int:id_cand>/', views.detalle_postulante, name='detalle_postulante'),
    path('seleccionar/', views.seleccionar_horario_puesto, name='seleccionar_horario_puesto'),
    path('seleccionar_vacante/', views.seleccionar_vacante, name='seleccionar_vacante'),
    path('preseleccion/', views.preseleccion_candidatos, name='preseleccion_candidatos'),
    path('seleccion_final/', views.seleccion_final, name='seleccion_final'),
    path('crear_vacante/', views.crear_vacante, name='crear_vacante'),
    path('listar_vacantes/', views.listar_vacantes, name='listar_vacantes'),
    path('programar_entrevista/', views.programar_entrevista, name='programar_entrevista'),
    path('listar_entrevistas/', views.listar_entrevistas, name='listar_entrevistas'),
    path('actualizar_evaluacion/', views.actualizar_evaluacion, name='actualizar_evaluacion'),
    path('listado_seleccionados/', views.listado_seleccionados, name='listado_seleccionados'),
    path('listar_evaluaciones/', views.listar_evaluaciones, name='listar_evaluaciones'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)