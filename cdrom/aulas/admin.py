from django.contrib import admin
from aulas.models import Aula


@admin.register(Aula)
class AulaAdmin(admin.ModelAdmin):
    list_display = ("institucion", "nombre", "capacidad_alumnos")
    list_filter = ("institucion",)
    search_fields = ("nombre",)
    ordering = ("nombre",)
