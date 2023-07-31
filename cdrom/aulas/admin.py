from django.contrib import admin
from aulas.models import (
    Aula,
    CaracteristicaAula,
    CaracteristicaEnAula,
    FotoAula,
)


@admin.register(Aula)
class AulaAdmin(admin.ModelAdmin):
    list_display = ("institucion", "nombre", "capacidad_alumnos")
    list_filter = ("institucion",)
    search_fields = ("nombre", "institucion__nombre")


@admin.register(FotoAula)
class FotoAulaAdmin(admin.ModelAdmin):
    list_display = ("aula", "descripcion", "orden")
    list_filter = ("aula", "aula__institucion")


@admin.register(CaracteristicaAula)
class CaracteristicaAulaAdmin(admin.ModelAdmin):
    list_display = ("nombre",)


@admin.register(CaracteristicaEnAula)
class CaracteristicaEnAulaAdmin(admin.ModelAdmin):
    list_display = ("aula", "caracteristica", "disponible", "se_debe_pedir")
    list_filter = ("aula", "caracteristica")
