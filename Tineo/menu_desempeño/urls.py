from django.urls import path
from . import views

urlpatterns=[
    path('menuDesempeño/',views.mostrarMenu)
]


