from django import forms
from .models import Tarea


class TareaForm(forms.ModelForm):
    class Meta:
        model = Tarea
        fields = ["descripcion", "prioridad", "fecha_limite", "tags"]
        widgets = {
            "fecha_limite": forms.DateInput(attrs={"type": "date"}),
        }
