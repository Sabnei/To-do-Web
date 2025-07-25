from django.shortcuts import render, redirect, get_object_or_404
from .models import Tarea
from .forms import TareaForm


# Create your views here.
def list_tareas(request):
    tareas = Tarea.objects.all()

    prioridad = request.GET.get("prioridad")
    etiqueta = request.GET.get("etiqueta")

    if prioridad:
        tareas = tareas.filter(prioridad=prioridad)

    if etiqueta:
        tareas = tareas.filter(tags__icontains=etiqueta)

    tareas = tareas.order_by("completado", "prioridad")

    return render(
        request,
        "tareas/lista_tareas.html",
        {
            "tareas": tareas,
            "prioridad_seleccionada": prioridad or "",
            "etiqueta": etiqueta or "",
        },
    )


def agregar_tarea(request):
    if request.method == "POST":
        form = TareaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("lista_tareas")
    else:
        form = TareaForm()
    return render(request, "tareas/agregar_tarea.html", {"form": form})


def completar_tarea(request, tarea_id):
    tarea = get_object_or_404(Tarea, id=tarea_id)
    tarea.competado = True
    tarea.save()
    return redirect("lista_tareas")


def eliminar_tarea(request, tarea_id):
    tarea = get_object_or_404(Tarea, id=tarea_id)
    tarea.delete()
    return redirect("lista_tareas")
