from django import forms
from django.forms import inlineformset_factory
from aulas.models import Aula, CaracteristicaEnAula, FotoAula


class AulaForm(forms.ModelForm):
    capacidad_alumnos = forms.IntegerField(min_value=1, max_value=200, required=True, label='Capacidad de alumnos')

    class Meta:
        model = Aula
        fields = '__all__'


AulasFeaturesFormSet = inlineformset_factory(
    Aula,
    CaracteristicaEnAula,
    fields=(
        'caracteristica',
        'disponible',
        'se_debe_pedir'
    ),
    extra=0,
    can_delete=True,
)


FotoAulasFormSet = inlineformset_factory(
    Aula,
    FotoAula,
    fields=(
        'foto',
        'orden',
        'descripcion'
    ),
    extra=0,
    can_delete=True,
)
