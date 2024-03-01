from django.db import models
from django.utils.text import slugify
from markdownfield.models import MarkdownField, RenderedMarkdownField
from markdownfield.validators import VALIDATOR_STANDARD
from Deutsche_Motors.base_model import AbstractBaseModel
from django.shortcuts import reverse
import random


class MainCarouselImage(models.Model):
    position = models.PositiveIntegerField(default=1)
    image = models.ImageField()

    class Meta:
        verbose_name = "Фотография карусели"
        verbose_name_plural = "Фотографии карусели"
        ordering = ("position",)

    def __str__(self):
        return str(self.image.name)


class Equipment(models.Model):
    text = models.CharField(max_length=255)
    translation = models.CharField(max_length=255)

    def __str__(self):
        return str(self.text)


class Car(AbstractBaseModel):
    image_url = models.URLField()
    title = models.CharField(max_length=255)
    price = models.PositiveIntegerField()

    technical_data = models.JSONField()
    equipment = models.ManyToManyField(Equipment)

    url = models.URLField()
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    class Meta:
        verbose_name = "Авто"
        verbose_name_plural = "Автомобили"

    @property
    def absolute_url(self):
        return reverse("product", kwargs={"slug": self.slug})

    @property
    def price_in_rub(self) -> int:
        return self.price * 80

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title + "-" + str(random.getrandbits(4)))
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.title)


class Article(AbstractBaseModel):
    image = models.ImageField()
    title = models.CharField(max_length=255)
    text = MarkdownField(rendered_field="text_rendered", validator=VALIDATOR_STANDARD)
    text_rendered = RenderedMarkdownField()

    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    @property
    def absolute_url(self):
        return reverse("blog-detail", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"

    def __str__(self):
        return str(self.title)
