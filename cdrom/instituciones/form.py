from django import forms
from django.forms import inlineformset_factory
from instituciones.models import Institucion, FotoInstitucion


class InstitucionForm(forms.ModelForm):
    class Meta:
        model = Institucion
        fields = ['nombre', 'logo', 'site']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'custom-class'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Update the widget for 'site' field to TextInput
        self.fields['site'].widget = forms.TextInput()


FotoInstitucionFormSet = inlineformset_factory(
    Institucion,
    FotoInstitucion,
    fields=(
        'foto',
        'orden',
        'descripcion'
    ),
    extra=1,
    can_delete=True,
)
