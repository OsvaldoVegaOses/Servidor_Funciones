# Generated by Django 5.0.6 on 2024-05-23 04:26

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("gestion_contactos", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="contact",
            name="name",
            field=models.CharField(max_length=255),
        ),
    ]
