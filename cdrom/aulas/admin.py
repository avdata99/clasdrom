from django.contrib import admin
from aulas.models import Aula, FotoAula


@admin.register(Aula)
class AulaAdmin(admin.ModelAdmin):
    list_display = ("institucion", "nombre", "capacidad_alumnos")
    list_filter = ("institucion",)
    search_fields = ("nombre",)
    ordering = ("nombre",)


@admin.register(FotoAula)
class FotoAulaAdmin(admin.ModelAdmin):
    list_display = ("aula", "descripcion", "orden")
    list_filter = ("aula",)
    ordering = ("orden",)
