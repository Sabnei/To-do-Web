from django.shortcuts import render, redirect, get_object_or_404
from .models import Tarea
from .forms import TareaForm


# Create your views here.
def list_tareas(request):
    tareas = Tarea.objects.all().order_by("completado", "prioridad")
    return render(request, "tareas/lista_tareas.html", {"tareas": tareas})


def agregar_tarea(request):
    if request.method == "POST":
        form = TareaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("lista_tareas")
    else:
        form = TareaForm()
    return render(request, "tareas/agregar_tarea.html", {"form": form})
