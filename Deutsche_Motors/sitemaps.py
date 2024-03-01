from django.contrib.sitemaps import Sitemap
from cars.models import Car


class CarSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return Car.objects.all()

    def lastmod(self, obj):
        pass  # return obj.publish
