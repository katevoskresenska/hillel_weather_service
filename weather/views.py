import requests
from django.http import JsonResponse
from django.shortcuts import render, redirect
from rest_framework import viewsets, status, generics
from rest_framework.response import Response

from weather.forms import CoordForm
from weather.forms import NameForm
from weather.models import Country
from weather.models import Location
from weather.models import Weather
from weather.serializers import WeatherSerializer

from rest_framework_swagger.views import get_swagger_view
from django.conf.urls import url

from utils import get_wiki_page
from utils import get_country_flag
from utils import construct_url

schema_view = get_swagger_view(title='Pastebin API')

urlpatterns = [
    url(r'^$', schema_view)
]


class WeatherRetrieveViewSet(generics.RetrieveAPIView):
    queryset = Weather.objects.all()
    serializer_class = WeatherSerializer

    def get(self, request, location):
        try:
            url = construct_url.UrlConstructor.construct_url_by_location(location)
        except Exception as exc:
            return exc.__doc__
        if url is not None:
            resp = requests.get(url).json()
        else:
            return JsonResponse("Error")
        country_name = resp["sys"]["country"]
        country, _ = Country.objects.get_or_create(
            name=country_name,
            defaults={
                'flag': get_country_flag.CountryFlagRetrieve.get_country_flag(country_name),
                'wiki_page': get_wiki_page.WikiPageRetrieve.get_wiki_page_by_country_code(country_name)
            }
        )
        location, _ = Location.objects.get_or_create(
            longitude=resp['coord']['lon'],
            latitude=resp['coord']['lat'],
            defaults={'city': resp['name'], 'country': country}
        )
        weather = Weather.objects.create(
            temperature=resp['main']['temp'],
            temp_feels_like=resp['main']['feels_like'],
            temp_min=resp['main']['temp_min'],
            temp_max=resp['main']['temp_max'],
            pressure=resp['main']['pressure'],
            humidity=resp['main']['humidity'],
            visibility=resp['visibility'],
            wind_speed=resp['wind']['speed'],
            wind_deg=resp['wind']['deg']
        )
        weather.location.add(location)
        queryset = Weather.objects.get(id=weather.id)
        serializer = WeatherSerializer(queryset)
        context = {'weathers': serializer.data}
        return JsonResponse(context)


class WeatherCreateViewSet(viewsets.ModelViewSet):
    queryset = Weather.objects.all()
    serializer_class = WeatherSerializer
    weather_list = list()
    context = {"weathers": weather_list}

    def creating(self, resp):
        country_name = resp["sys"]["country"]
        country, _ = Country.objects.get_or_create(
            name=country_name,
            defaults={
                "flag": get_country_flag.CountryFlagRetrieve.get_country_flag(country_name),
                "wiki_page": get_wiki_page.WikiPageRetrieve.get_wiki_page_by_country_code(country_name),
            },
        )
        location, _ = Location.objects.get_or_create(
            longitude=resp["coord"]["lon"],
            latitude=resp["coord"]["lat"],
            defaults={"city": resp["name"], "country": country},
        )
        weather = self.queryset.create(
            temperature=resp["main"]["temp"],
            temp_feels_like=resp["main"]["feels_like"],
            temp_min=resp["main"]["temp_min"],
            temp_max=resp["main"]["temp_max"],
            pressure=resp["main"]["pressure"],
            humidity=resp["main"]["humidity"],
            visibility=resp["visibility"],
            wind_speed=resp["wind"]["speed"],
            wind_deg=resp["wind"]["deg"],
        )
        weather.location.add(location)
        queryset = Weather.objects.get(id=weather.id)
        serializer = WeatherSerializer(queryset)

        for weather_data in serializer.data.get("location"):
            res = {
                "city": weather_data["city"],
                "temperature": serializer.data.get("temperature"),
                "flag": weather_data["country"]["flag"],
                "wiki_page": weather_data["country"]["wiki_page"]
            }
            self.weather_list.append(res)

    def create(self, request, *args, **kwargs):
        form_city = NameForm(request.POST)
        form_coord = CoordForm(request.POST)
        url = None
        if form_city.is_valid():
            city = form_city.cleaned_data["city"]
            url = construct_url.UrlConstructor.construct_url_by_city(city)

        elif form_coord.is_valid():
            lat = form_coord.cleaned_data["lat"]
            lon = form_coord.cleaned_data["lon"]
            url = construct_url.UrlConstructor.construct_url_by_coordinates(lat, lon)

        if url is not None:
            resp = requests.get(url).json()
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        self.creating(resp)

        return redirect("/weather")

    def list(self, request, *args, **kwargs):
        super().list(request, *args, **kwargs)
        return render(request, "weather/index.html", {"weathers": self.weather_list})
