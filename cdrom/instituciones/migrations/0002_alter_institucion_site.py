# Generated by Django 4.2.3 on 2023-08-10 16:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0002_alter_domain_unique'),
        ('instituciones', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='institucion',
            name='site',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='sites.site'),
        ),
    ]