# Generated by Django 4.2.7 on 2023-12-06 16:39

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("cars", "0002_car_equipment"),
    ]

    operations = [
        migrations.CreateModel(
            name="Equipment",
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
                ("text", models.CharField(max_length=255)),
            ],
        ),
        migrations.RemoveField(
            model_name="car",
            name="equipment",
        ),
        migrations.AddField(
            model_name="car",
            name="equipment",
            field=models.ManyToManyField(to="cars.equipment"),
        ),
    ]
