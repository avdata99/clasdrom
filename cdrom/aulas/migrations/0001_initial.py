# Generated by Django 4.1.4 on 2022-12-24 05:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("instituciones", "0002_alter_institucion_logo"),
    ]

    operations = [
        migrations.CreateModel(
            name="Aula",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nombre", models.CharField(max_length=100)),
                ("capacidad_alumnos", models.IntegerField()),
                (
                    "institucion",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="instituciones.institucion",
                    ),
                ),
            ],
        ),
    ]
