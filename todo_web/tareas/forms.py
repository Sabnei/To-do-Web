from django import forms
from .models import Tarea


class TareaForm(forms.ModelForm):
    class Meta:
        model = Tarea
        fields = ["descripcion", "prioridad", "fecha_limite", "tags"]
        widgets = {
            "descripcion": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Describe tu tarea aquí..."
            }),
            "prioridad": forms.Select(attrs={
                "class": "form-select"
            }),
            "fecha_limite": forms.DateInput(attrs={
                "type": "date",
                "class": "form-control"
            }),
            "tags": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "trabajo, urgente, proyecto"
            }),
        }
