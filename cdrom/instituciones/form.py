from django import forms
from django.forms import inlineformset_factory
from instituciones.models import Institucion, FotoInstitucion


class InstitucionForm(forms.ModelForm):
    class Meta:
        model = Institucion
        fields = ['nombre', 'logo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'custom-class'}),
        }


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
