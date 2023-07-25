# Generated by Django 4.2.3 on 2023-07-20 23:02

from django.db import migrations, models
import django.db.models.deletion
import profesores.helpers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("core", "0002_persona"),
    ]

    operations = [
        migrations.CreateModel(
            name="Profesor",
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
                    "profe_id",
                    models.CharField(
                        default=profesores.helpers.generar_profe_id, max_length=100
                    ),
                ),
            ],
            bases=("core.persona",),
        ),
    ]