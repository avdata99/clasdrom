# Generated by Django 4.1.4 on 2022-12-26 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("instituciones", "0002_alter_institucion_logo"),
    ]

    operations = [
        migrations.AlterField(
            model_name="institucion",
            name="logo",
            field=models.ImageField(
                blank=True, null=True, upload_to="media/imgs/instituciones"
            ),
        ),
    ]
