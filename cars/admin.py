from django.contrib import admin
from .models import Car, Article, MainCarouselImage, Equipment
from .forms import AddCarForm, EditCarForm


admin.site.register(Car)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "slug")
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Equipment)
