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

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('registrar/', views.registrar_postulante, name='registrar_postulante'),
    path('seleccionar/', views.seleccionar_horario_puesto, name='seleccionar_horario_puesto'),
    path('preseleccion/', views.preseleccion_candidatos, name='preseleccion_candidatos'),
    path('seleccion_final/', views.seleccion_final, name='seleccion_final'),
    path('crear_perfil/', views.crear_perfil, name='crear_perfil'),
    path('programar_entrevista/', views.programar_entrevista, name='programar_entrevista'),
    path('actualizar_evaluacion/', views.actualizar_evaluacion, name='actualizar_evaluacion'),
]
