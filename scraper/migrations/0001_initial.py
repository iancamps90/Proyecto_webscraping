# Generated by Django 5.1.7 on 2025-03-18 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Oposicion",
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
                ("titulo", models.CharField(max_length=255)),
                ("entidad", models.CharField(max_length=255)),
                ("fecha_publicacion", models.DateField()),
                ("fecha_limite", models.DateField(blank=True, null=True)),
                ("requisitos", models.TextField(blank=True)),
                ("enlace", models.URLField(unique=True)),
            ],
        ),
    ]
