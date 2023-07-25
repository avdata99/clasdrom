# Generated by Django 4.2.3 on 2023-07-20 23:02

import alumnos.helpers
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("core", "0002_persona"),
    ]

    operations = [
        migrations.CreateModel(
            name="Alumno",
            fields=[
                (
                    "persona_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="core.persona",
                    ),
                ),
                (
                    "matricula_id",
                    models.CharField(
                        default=alumnos.helpers.generar_matricula_id, max_length=100
                    ),
                ),
            ],
            bases=("core.persona",),
        ),
    ]
