from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.core.exceptions import ObjectDoesNotExist
from django.utils.text import slugify
from cars.utils.parser import parse_by_link, parse_price
import random
import locale
from .models import Article, Car, MainCarouselImage, Equipment


def index_view(request):
    images = MainCarouselImage.objects.order_by("position")[:8]
    cars = Car.objects.all()[:5]
    articles = Article.objects.all()[:5]
    print(cars)
    if request.POST:
        price = parse_price(request.POST.get("link"))
        if price == -1:
            return render(
                request,
                "cars/index.html",
                {"error": "Машина не найдена. Проверьте ссылку", "images": images, "cars": cars, "articles": articles},
            )
        print(f"Price: {price:,.2f} ₽")

        return render(
            request,
            "cars/index.html",
            {"price": f"{price:,.2f} ₽", "link": request.POST.get("link"), "images": images, "cars": cars, "articles": articles},
        )
    else:
        return render(
            request,
            "cars/index.html",
            {"images": images, "cars": cars, "articles": articles},
        )


def car_detail_view(request, slug):
    car = get_object_or_404(Car, slug=slug)
    equipments = car.equipment.all()
    if request.GET:
        fullname = request.POST.get("fullname")
        phone = request.POST.get("phone")
        # and here <
    else:
        return render(
            request, "cars/car_detail.html", {"car": car, "equipments": equipments}
        )


def catalog_view(request):
    cars = Car.objects.all()
    return render(request, "cars/catalog.html", {"cars": cars})


def blog_view(request):
    articles = Article.objects.all()
    return render(request, "cars/blog.html", {"articles": articles})


def blog_detail_view(request, slug):
    article = get_object_or_404(Article, slug=slug)
    return render(request, "cars/blog_detail.html", {"article": article})


def calculator_view(request):
    if request.POST:
        price = parse_price(request.POST.get("link"))
        if price == -1:
            return render(
                request,
                "cars/calculator.html",
                {"error": "Машина не найдена. Проверьте ссылку"},
            )
        print(f"Price: {price:,.2f} ₽")

        return render(
            request,
            "cars/calculator.html",
            {"price": f"{price:,.2f} ₽", "link": request.POST.get("link")},
        )

    return render(request, "cars/calculator.html")  # Путь к вашему шаблону


def parser_view(request):
    if request.POST:
        car = parse_by_link(request.POST.get("link"))
        car_model = Car(
            slug=slugify(car["title"] + "-" + str(random.getrandbits(4))),
            title=car["title"],
            price=car["price"],
            image_url=car["image_url"],
            technical_data=car["technical_data"],
        )
        car_model.save()

        for equipment_string in car["equipment"]:
            try:
                equipment = Equipment.objects.get(text=equipment_string)
            except ObjectDoesNotExist:
                # Create a new Equipment object if it doesn't exist
                equipment = Equipment(text=equipment_string, translation="")
                equipment.save()

            car_model.equipment.add(equipment)

        car_model.save()
        return render(
            request,
            "cars/parser.html",
            {
                "car": car_model,
                "technical_data": car_model.technical_data.items(),
                "equipment": car["equipment"],
            },
        )

    return render(request, "cars/parser.html")
