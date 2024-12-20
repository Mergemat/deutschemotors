from django.db import models
from django.utils.translation import gettext_lazy as _


class AbstractBaseModel(models.Model):
    """Базовая модель"""

    created_at = models.DateTimeField(_("Создан"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Изменен"), auto_now=True)

    class Meta:
        abstract = True
        ordering = ["-id"]
