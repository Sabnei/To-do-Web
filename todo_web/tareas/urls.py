from django.urls import path
from . import views

urlpatterns = {
    path("", views.list_tareas, name="lista_tareas"),
    path("agregar/", views.agregar_tarea, name="agregar_tarea"),
    path(
        "completar/<int:tarea_id>/",
        views.completar_tarea,
        name="completar_tarea",
    ),
    path(
        "eliminar/<int:tarea_id>/", views.eliminar_tarea, name="eliminar_tarea"
    ),
}

