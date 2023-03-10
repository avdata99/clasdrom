# Generated by Django 4.1.4 on 2022-12-24 05:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Institucion",
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
                (
                    "logo",
                    models.ImageField(blank=True, null=True, upload_to="instituciones"),
                ),
            ],
        ),
    ]
