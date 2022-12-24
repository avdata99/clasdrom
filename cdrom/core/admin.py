from django.contrib import admin
from core.models import Celular


@admin.register(Celular)
class CelularAdmin(admin.ModelAdmin):
    list_display = ("codigo_pais", "codigo_area", "numero")
    list_filter = ("codigo_area",)
    search_fields = ("numero",)
    ordering = ("codigo_area", "numero")
