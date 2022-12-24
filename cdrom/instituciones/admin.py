from django.contrib import admin
from instituciones.models import Institucion


@admin.register(Institucion)
class InstitucionAdmin(admin.ModelAdmin):
    list_display = ("nombre",)
