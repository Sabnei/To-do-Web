from django.db import models


# Create your models here.
class Tarea(models.Model):
    PRIORIDADES = [("alta", "Alta"), ("media", "Media"), ("baja", "Baja")]

    descripcion = models.CharField(max_length=255)
    completado = models.BooleanField(default=False)
    prioridad = models.CharField(max_length=10, choices=PRIORIDADES)
    fecha_limite = models.DateField(null=True, blank=True)
    tags = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.descripcion
