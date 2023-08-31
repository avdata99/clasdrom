from django import forms
from django.forms import inlineformset_factory
from .models import Alumno
from core.models import Celular
from django.contrib.sites.models import Site
from alumnos.helpers import generar_matricula_id


class AlumnoForm(forms.ModelForm):

    matricula_id = forms.CharField(max_length=100, initial=generar_matricula_id, widget=forms.HiddenInput)

    class Meta:
        model = Alumno
        fields = '__all__'

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        # # Update the widget for 'site' field to TextInput
        # self.fields['site'].widget = forms.TextInput()

        # # Update the widget for 'celular_principal' field to TextInput
        # self.fields['celular_principal'].widget = forms.TextInput()
AlumnoCelFeaturesFormSet = inlineformset_factory(
    Alumno,
    fields=(
        'codigo_pais',
        'codigo_area',
        'numero'
    ),
    extra=1,
    can_delete=True,
)


AlumnoSiteFormSet = inlineformset_factory(
    Alumno,
    fields=(
        'domain',
        'name',
        'descripcion'
    ),
    extra=1,
    can_delete=True,
)
