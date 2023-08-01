# Generated by Django 4.2.3 on 2023-08-01 16:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('instituciones', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Curso',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=100)),
                ('descripcion', models.TextField(blank=True, null=True)),
                ('institucion', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='instituciones.institucion')),
            ],
        ),
    ]