from django import forms
from .models import Alumno
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
