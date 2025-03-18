# Generated by Django 5.1.7 on 2025-03-18 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("scraper", "0003_ayuntamiento_comunidad"),
    ]

    operations = [
        migrations.AddField(
            model_name="oposicion",
            name="categoria",
            field=models.CharField(
                choices=[
                    ("Administrativo", "Administrativo"),
                    ("Policía Local", "Policía Local"),
                    ("Bomberos", "Bomberos"),
                    ("Sanidad", "Sanidad"),
                    ("Educación", "Educación"),
                    ("Ingeniería", "Ingeniería"),
                    ("Otros", "Otros"),
                ],
                default="Otros",
                max_length=50,
            ),
        ),
        migrations.AddField(
            model_name="oposicion",
            name="comunidad",
            field=models.CharField(default="Valencia", max_length=100),
        ),
    ]
