from django.urls import path
from . import views

urlpatterns=[
    path('revisar/',views.baseRevisar),
    path('revisar/apellido/',views.revisarApellido),
    path('revisar/<id_tipo_cuestionario>/',views.revisarTipoCuestionario),
    path('responder/calificacion/NULL/',views.revisarCalificacionNULL),
    path('responder/calificacion/<id_tipo_calificacion>/',views.revisarCalificacion)
]



