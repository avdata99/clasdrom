from django import forms
from .models import Aula, CaracteristicaAula, CaracteristicaEnAula


class CaracteristicaForm(forms.ModelForm):
    disponible = forms.BooleanField()
    se_debe_pedir = forms.BooleanField()


class AulaCreateForm(forms.ModelForm):
    caracteristicas = forms.ModelMultipleChoiceField(
        queryset=CaracteristicaAula.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Aula
        fields = ['institucion', 'nombre', 'descripcion', 'capacidad_alumnos', 'caracteristicas']

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
        if caracteristicas is not None:
            for caracteristica in caracteristicas:
                # Obtener la relación entre Aula y CaracteristicaAula desde la tabla CaracteristicaEnAula
                relacion = CaracteristicaEnAula.objects.filter(aula=self.instance, caracteristica=caracteristica).first()
                if relacion:
                    if not relacion.disponible and not relacion.se_debe_pedir:
                        raise forms.ValidationError("La característica debe estar disponible o ser solicitada.")
        return cleaned_data
