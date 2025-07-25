from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from urllib.parse import unquote
from .models import Tarea
from .forms import TareaForm


# Create your views here.
def inicio(request):
    """Vista para la página de inicio con estadísticas"""
    total_tareas = Tarea.objects.count()
    tareas_completadas = Tarea.objects.filter(completado=True).count()
    tareas_pendientes = Tarea.objects.filter(completado=False).count()
    
    # Tareas por prioridad
    tareas_alta = Tarea.objects.filter(prioridad='alta', completado=False).count()
    tareas_media = Tarea.objects.filter(prioridad='media', completado=False).count()
    tareas_baja = Tarea.objects.filter(prioridad='baja', completado=False).count()
    
    # Tareas recientes (últimas 5)
    tareas_recientes = Tarea.objects.order_by('-id')[:5]
    
    # Tareas urgentes (alta prioridad y pendientes)
    tareas_urgentes = Tarea.objects.filter(prioridad='alta', completado=False)[:3]
    
    context = {
        'total_tareas': total_tareas,
        'tareas_completadas': tareas_completadas,
        'tareas_pendientes': tareas_pendientes,
        'tareas_alta': tareas_alta,
        'tareas_media': tareas_media,
        'tareas_baja': tareas_baja,
        'tareas_recientes': tareas_recientes,
        'tareas_urgentes': tareas_urgentes,
    }
    
    return render(request, 'tareas/inicio.html', context)


def lista_tareas(request):
    tareas = Tarea.objects.all()

    prioridad = request.GET.get("prioridad")
    etiqueta = request.GET.get("etiqueta")
    completado = request.GET.get("completado")

    if prioridad:
        tareas = tareas.filter(prioridad=prioridad)

    if etiqueta:
        tareas = tareas.filter(tags__icontains=etiqueta)

    if completado == "completado":
        tareas = tareas.filter(completado=True)
    elif completado == "pendiente":
        tareas = tareas.filter(completado=False)

    tareas = tareas.order_by("completado", "prioridad")

    return render(
        request,
        "tareas/lista_tareas.html",
        {
            "tareas": tareas,
            "prioridad_seleccionada": prioridad or "",
            "etiqueta": etiqueta or "",
            "estado_seleccionado": completado or "",
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
    tarea.completado = not tarea.completado
    tarea.save()
    return redirect("lista_tareas")


def eliminar_tarea(request, tarea_id):
    tarea = get_object_or_404(Tarea, id=tarea_id)
    tarea.delete()
    return redirect("lista_tareas")


def exportar_pdf(request):
    tareas = Tarea.objects.all()

    prioridad = request.GET.get("prioridad")
    etiqueta = request.GET.get("etiqueta")

    if prioridad:
        tareas = tareas.filter(prioridad=prioridad)
    if etiqueta:
        tareas = tareas.filter(tags__icontains=etiqueta)

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="tareas.pdf"'

    c = canvas.Canvas(response, pagesize=letter)
    width, height = letter
    y = height - 40

    c.setFont("Helvetica-Bold", 16)
    c.drawString(40, y, "Lista de Tareas")
    y -= 30

    if prioridad:
        c.setFont("Helvetica", 12)
        c.drawString(40, y, f"Filtro - Prioridad: {prioridad}")
        y -= 15
    if etiqueta:
        c.drawString(40, y, f"Filtro - Etiqueta contiene: {etiqueta}")
        y -= 15
    y -= 10

    for t in tareas:
        if y < 60:
            c.showPage()
            y = height - 40

        estado = "✔" if t.completado else "✖"
        c.setFont("Helvetica-Bold", 12)
        c.setFillColor(colors.black)
        c.drawString(
            40,
            y,
            f"{t.id}. [{estado}] {t.descripcion} (Prioridad: {t.prioridad})",
        )
        y -= 18

        if t.fecha_limite:
            c.setFont("Helvetica", 10)
            c.drawString(60, y, f"Fecha límite: {t.fecha_limite}")
            y -= 14

        if t.tags:
            c.drawString(60, y, f"Etiquetas: {t.tags}")
            y -= 14

        y -= 6
        c.setStrokeColor(colors.lightgrey)
        c.line(40, y, width - 40, y)
        y -= 10

    c.save()
    return response
