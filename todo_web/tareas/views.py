from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from urllib.parse import unquote
from .models import Tarea
from .forms import TareaForm


class TareaFilterMixin:
    """Mixin para aplicar filtros comunes a las tareas"""

    def apply_filters(self, queryset):
        """Aplicar filtros comunes a un queryset de tareas"""
        prioridad = self.request.GET.get("prioridad")
        etiqueta = self.request.GET.get("etiqueta")
        completado = self.request.GET.get("completado")

        if prioridad:
            queryset = queryset.filter(prioridad=prioridad)
        if etiqueta:
            queryset = queryset.filter(tags__icontains=etiqueta)
        if completado == "completado":
            queryset = queryset.filter(completado=True)
        elif completado == "pendiente":
            queryset = queryset.filter(completado=False)

        return queryset

    def get_filter_context(self):
        """Obtener contexto de filtros para templates"""
        return {
            "prioridad_seleccionada": self.request.GET.get("prioridad", ""),
            "etiqueta": self.request.GET.get("etiqueta", ""),
            "estado_seleccionado": self.request.GET.get("completado", ""),
        }


class TareaListView(TareaFilterMixin, ListView):
    """Vista basada en clase para listar tareas con filtros"""

    model = Tarea
    template_name = "tareas/lista_tareas.html"
    context_object_name = "tareas"

    def get_queryset(self):
        """Aplicar filtros a las tareas"""
        queryset = Tarea.objects.all()
        return self.apply_filters(queryset).order_by("completado", "prioridad")

    def get_context_data(self, **kwargs):
        """Agregar datos de contexto para los filtros"""
        context = super().get_context_data(**kwargs)
        context.update(self.get_filter_context())
        return context


class TareaCreateView(CreateView):
    """Vista basada en clase para crear tareas"""

    model = Tarea
    form_class = TareaForm
    template_name = "tareas/agregar_tarea.html"
    success_url = reverse_lazy("lista_tareas")

    def form_valid(self, form):
        """Mensaje de éxito al crear tarea"""
        messages.success(self.request, "Tarea creada exitosamente.")
        return super().form_valid(form)


class TareaService:
    """Clase de servicio para operaciones comunes con tareas"""

    @staticmethod
    def get_filtered_tareas(request):
        """Obtener tareas filtradas"""
        tareas = Tarea.objects.all()

        prioridad = request.GET.get("prioridad")
        etiqueta = request.GET.get("etiqueta")

        if prioridad:
            tareas = tareas.filter(prioridad=prioridad)
        if etiqueta:
            tareas = tareas.filter(tags__icontains=etiqueta)

        return tareas

    @staticmethod
    def get_statistics():
        """Obtener estadísticas de tareas"""
        total_tareas = Tarea.objects.count()
        tareas_completadas = Tarea.objects.filter(completado=True).count()
        tareas_pendientes = Tarea.objects.filter(completado=False).count()

        # Tareas por prioridad
        tareas_alta = Tarea.objects.filter(
            prioridad="alta", completado=False
        ).count()
        tareas_media = Tarea.objects.filter(
            prioridad="media", completado=False
        ).count()
        tareas_baja = Tarea.objects.filter(
            prioridad="baja", completado=False
        ).count()

        return {
            "total_tareas": total_tareas,
            "tareas_completadas": tareas_completadas,
            "tareas_pendientes": tareas_pendientes,
            "tareas_alta": tareas_alta,
            "tareas_media": tareas_media,
            "tareas_baja": tareas_baja,
        }

    @staticmethod
    def get_recent_tareas(limit=5):
        """Obtener tareas recientes"""
        return Tarea.objects.order_by("-id")[:limit]

    @staticmethod
    def get_urgent_tareas(limit=3):
        """Obtener tareas urgentes (alta prioridad y pendientes)"""
        return Tarea.objects.filter(prioridad="alta", completado=False)[:limit]


class PDFGenerator:
    """Clase para generar PDFs de tareas"""

    @staticmethod
    def create_pdf_content(canvas_obj, tareas, prioridad=None, etiqueta=None):
        """Crear el contenido del PDF"""
        width, height = letter
        y = height - 40

        # Título
        canvas_obj.setFont("Helvetica-Bold", 16)
        canvas_obj.drawString(40, y, "Lista de Tareas")
        y -= 30

        # Filtros aplicados
        if prioridad or etiqueta:
            canvas_obj.setFont("Helvetica", 12)
            if prioridad:
                canvas_obj.drawString(
                    40, y, f"Filtro - Prioridad: {prioridad}"
                )
                y -= 15
            if etiqueta:
                canvas_obj.drawString(
                    40, y, f"Filtro - Etiqueta contiene: {etiqueta}"
                )
                y -= 15
            y -= 10

        # Contenido de tareas
        for tarea in tareas:
            if y < 60:
                canvas_obj.showPage()
                y = height - 40

            estado = "✔" if tarea.completado else "✖"
            canvas_obj.setFont("Helvetica-Bold", 12)
            canvas_obj.setFillColor(colors.black)
            canvas_obj.drawString(
                40,
                y,
                f"{tarea.id}. [{estado}] {tarea.descripcion} (Prioridad: {tarea.prioridad})",
            )
            y -= 18

            if tarea.fecha_limite:
                canvas_obj.setFont("Helvetica", 10)
                canvas_obj.drawString(
                    60, y, f"Fecha límite: {tarea.fecha_limite}"
                )
                y -= 14

            if tarea.tags:
                canvas_obj.drawString(60, y, f"Etiquetas: {tarea.tags}")
                y -= 14

            y -= 6
            canvas_obj.setStrokeColor(colors.lightgrey)
            canvas_obj.line(40, y, width - 40, y)
            y -= 10


def inicio(request):
    """Vista para la página de inicio con estadísticas"""
    # Usar el servicio para obtener datos
    service = TareaService()
    stats = service.get_statistics()
    tareas_recientes = service.get_recent_tareas()
    tareas_urgentes = service.get_urgent_tareas()

    context = {
        **stats,
        "tareas_recientes": tareas_recientes,
        "tareas_urgentes": tareas_urgentes,
    }

    return render(request, "tareas/inicio.html", context)


def completar_tarea(request, tarea_id):
    """Cambiar el estado de completado de una tarea"""
    tarea = get_object_or_404(Tarea, id=tarea_id)
    tarea.completado = not tarea.completado
    tarea.save()

    # Mensaje de confirmación
    estado = "completada" if tarea.completado else "marcada como pendiente"
    messages.success(request, f'Tarea "{tarea.descripcion}" {estado}.')

    return redirect("lista_tareas")


def eliminar_tarea(request, tarea_id):
    """Eliminar una tarea"""
    tarea = get_object_or_404(Tarea, id=tarea_id)
    descripcion = tarea.descripcion
    tarea.delete()

    messages.success(request, f'Tarea "{descripcion}" eliminada exitosamente.')
    return redirect("lista_tareas")


def exportar_pdf(request):
    """Exportar tareas a PDF"""
    # Usar el servicio para obtener tareas filtradas
    service = TareaService()
    tareas = service.get_filtered_tareas(request)

    prioridad = request.GET.get("prioridad")
    etiqueta = request.GET.get("etiqueta")

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="tareas.pdf"'

    c = canvas.Canvas(response, pagesize=letter)

    # Usar la clase PDFGenerator para crear el contenido
    PDFGenerator.create_pdf_content(c, tareas, prioridad, etiqueta)

    c.save()
    return response


# Mantener las vistas originales como alias para compatibilidad
lista_tareas = TareaListView.as_view()
agregar_tarea = TareaCreateView.as_view()
