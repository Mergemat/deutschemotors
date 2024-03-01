# Generated by Django 4.2.7 on 2023-12-05 17:38

from django.db import migrations, models
import markdownfield.models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Article",
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
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="Создан"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="Изменен"),
                ),
                ("image", models.ImageField(upload_to="")),
                ("title", models.CharField(max_length=255)),
                (
                    "text",
                    markdownfield.models.MarkdownField(rendered_field="text_rendered"),
                ),
                ("text_rendered", markdownfield.models.RenderedMarkdownField()),
                ("slug", models.SlugField(max_length=255, unique=True)),
            ],
            options={
                "verbose_name": "Статья",
                "verbose_name_plural": "Статьи",
            },
        ),
        migrations.CreateModel(
            name="Car",
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
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="Создан"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="Изменен"),
                ),
                ("image_url", models.URLField()),
                ("title", models.CharField(max_length=255)),
                ("price", models.PositiveIntegerField()),
                ("technical_data", models.JSONField()),
                ("url", models.URLField()),
                ("slug", models.SlugField(max_length=255, unique=True)),
            ],
            options={
                "verbose_name": "Авто",
                "verbose_name_plural": "Автомобили",
            },
        ),
        migrations.CreateModel(
            name="MainCarouselImage",
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
                ("position", models.PositiveIntegerField(default=1)),
                ("image", models.ImageField(upload_to="")),
            ],
            options={
                "verbose_name": "Фотография карусели",
                "verbose_name_plural": "Фотографии карусели",
                "ordering": ("position",),
            },
        ),
    ]
