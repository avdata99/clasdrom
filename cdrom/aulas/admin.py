from django.contrib import admin
from aulas.models import Aula


@admin.register(Aula)
class AulaAdmin(admin.ModelAdmin):
    list_display = ("codigo_pais", "codigo_area", "numero")
    list_filter = ("codigo_area",)
    search_fields = ("numero",)
    ordering = ("codigo_area", "numero")
