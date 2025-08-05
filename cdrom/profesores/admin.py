from django.contrib import admin
from profesores.models import Profesor


@admin.register(Profesor)
class ProfesorAdmin(admin.ModelAdmin):
    list_display = ("apellidos", "nombres", "profe_id")
    search_fields = ("apellidos", "nombres", "profe_id",)
    readonly_fields = ("profe_id",)
