from django import forms
from django.forms import inlineformset_factory
from aulas.models import Aula, CaracteristicaEnAula


class AulaForm(forms.ModelForm):
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
    extra=2,
    can_delete=True,
)
