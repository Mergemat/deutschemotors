from django.contrib import admin
from .models import Car, Article, MainCarouselImage, Equipment
from .forms import AddCarForm, EditCarForm


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        if obj is None:
            return AddCarForm
        else:
            return EditCarForm


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "slug")
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(MainCarouselImage)
admin.site.register(Equipment)
