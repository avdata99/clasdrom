# Generated by Django 4.2.3 on 2023-07-31 19:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

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
                ("descripcion", models.TextField(blank=True, null=True)),
                ("capacidad_alumnos", models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name="CaracteristicaAula",
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
                (
                    "nombre",
                    models.CharField(
                        help_text="Por ejemplo AC, Proyector, Pizarra, etc.",
                        max_length=100,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="FotoAula",
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
                ("foto", models.ImageField(upload_to="imgs/aulas")),
                ("orden", models.IntegerField(default=100)),
                ("descripcion", models.TextField(blank=True, null=True)),
                (
                    "aula",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="fotos",
                        to="aulas.aula",
                    ),
                ),
            ],
            options={
                "ordering": ["orden"],
            },
        ),
        migrations.CreateModel(
            name="CaracteristicaEnAula",
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
                ("descripcion", models.TextField(blank=True, null=True)),
                (
                    "disponible",
                    models.BooleanField(default=True, help_text="Está disponible?"),
                ),
                (
                    "se_debe_pedir",
                    models.BooleanField(
                        default=False,
                        help_text="No es una caracteristica fija y se debe pedir?",
                    ),
                ),
                ("orden", models.IntegerField(default=100)),
                (
                    "aula",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="caracteristicas",
                        to="aulas.aula",
                    ),
                ),
                (
                    "caracteristica",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="en_aulas",
                        to="aulas.caracteristicaaula",
                    ),
                ),
            ],
            options={
                "ordering": ["orden"],
            },
        ),
    ]
