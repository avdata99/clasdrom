from django.contrib import admin
from alumnos.models import Alumno


@admin.register(Alumno)
class AlumnoAdmin(admin.ModelAdmin):
    list_display = ("apellidos", "nombres", "matricula_id")
    list_filter = ("site",)
    search_fields = ("apellidos", "nombres", "matricula_id",)
    readonly_fields = ("matricula_id",)
