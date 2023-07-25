from django import forms
from .models import Aula


class AulaCreateForm(forms.ModelForm):
    class Meta:
        model = Aula
        fields = ['institucion', 'nombre', 'descripcion', 'capacidad_alumnos']

    # Agregar validación personalizada para la capacidad de alumnos
    def clean_capacidad_alumnos(self):
        capacidad_alumnos = self.cleaned_data.get('capacidad_alumnos')
        if capacidad_alumnos <= 0:
            raise forms.ValidationError("La capacidad de alumnos debe ser mayor a cero.")
        return capacidad_alumnos

    # Agregar validación personalizada para las características del aula
    def clean(self):
        cleaned_data = super().clean()
        caracteristicas = cleaned_data.get('caracteristicas')
        for caracteristica in caracteristicas:
            if not caracteristica.disponible and not caracteristica.se_debe_pedir:
                raise forms.ValidationError("La característica debe estar disponible o ser solicitada.")
        return cleaned_data
