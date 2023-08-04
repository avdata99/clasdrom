from django import forms
from profesores.models import Profesor
from profesores.helpers import generar_profe_id


class ProfesorForm(forms.ModelForm):
    profe_id = forms.CharField(max_length=100, initial=generar_profe_id, widget=forms.HiddenInput)

    class Meta:
        model = Profesor
        fields = '__all__'

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        # Update the widget for 'site' field to TextInput
        self.fields['site'].widget = forms.TextInput()

        # Update the widget for 'celular_principal' field to TextInput
        self.fields['celular_principal'].widget = forms.TextInput()
