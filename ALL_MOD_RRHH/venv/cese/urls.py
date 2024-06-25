from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('seleccion/', views.seleccion, name='seleccion'),
    path('cese1/', views.cese1, name='cese1'),
    path('cese2/<int:id_cese>/', views.cese2, name='cese2'),
    path('cese3/', views.cese3, name='cese3'),
    path('cese4/', views.cese4, name='cese4'),
    path('cese5/', views.cese5, name='cese5'),
    path('cese6/', views.cese6, name='cese6'),
    path('cese7/', views.cese7, name='cese7')
]