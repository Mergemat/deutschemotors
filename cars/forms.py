from django import forms

from Deutsche_Motors.utils import parse_car_data

from .models import Car


class AddCarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ["url"]

    def clean_url(self):
        url = self.cleaned_data.get("url")
        # data = parse_car_data(url)
        # self.instance.title = data.title
        # self.instance.price = data.price
        # self.instance.image_url = data.image_url
        # self.instance.technical_data = data.tech_data
        self.instance.title = "data.title"
        self.instance.price = 123
        self.instance.image_url = "https://google.com/"
        self.instance.technical_data = {"Fahrzeugzustand": "Unfallfrei"}
        self.instance.equipment = ["ABS", "Allwetterreifen"]
        return url


class EditCarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = "__all__"
