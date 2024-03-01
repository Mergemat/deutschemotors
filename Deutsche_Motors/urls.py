from django.contrib import admin
from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static
from cars.views import (
    index_view,
    car_detail_view,
    blog_detail_view,
    catalog_view,
    blog_view,
    parser_view,
)
from django.views.generic import TemplateView
from django.contrib.sitemaps.views import sitemap
from .sitemaps import CarSitemap

sitemaps = {
    "cars": CarSitemap,
}

urlpatterns = [
    path("admin/", admin.site.urls),
    path("parser/", parser_view),
    path("", index_view, name="index"),
    path("blog/", blog_view, name="blog"),
    path("catalog/", catalog_view, name="catalog"),
    path("product/<slug:slug>/", car_detail_view, name="product"),
    path("blog/<slug:slug>/", blog_detail_view, name="blog-detail"),
    re_path(
        r"^robots\.txt$",
        TemplateView.as_view(
            template_name="Deutsche_Motors/robots.txt", content_type="text/plain"
        ),
    ),
    re_path(
        r"^sitemap\.xml$",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
