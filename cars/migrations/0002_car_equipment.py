# Generated by Django 4.2.7 on 2023-12-06 16:29

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("cars", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="car",
            name="equipment",
            field=models.JSONField(default=[]),
        ),
    ]
