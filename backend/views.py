from django.shortcuts import render, redirect
import requests
from .models import City
from .forms import CityForm


def home(request):
    err_msg = ''
    succ_msg = ''
    api_key = "4ce021640c50883dfd597628f83985f0"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"

    if request.method == "POST":
        form = CityForm(request.POST)
        if form.is_valid():
            new_city = form.cleaned_data['city_name'].lower()
            existing_city = City.objects.filter(city_name=new_city).count()

        if existing_city == 0:
            complete_url = base_url + "appid=" + \
                api_key + "&q=" + str(new_city)
            response = requests.get(complete_url)
            response_json = response.json()
            if response_json['cod'] == 200:
                form.save()
                succ_msg = 'City Added successfully.'
            else:
                err_msg = 'City Not found!'
        else:
            err_msg = 'City in database'

    form = CityForm()

    cities = City.objects.all()
    weather_data = []

    for city in cities:
        complete_url = base_url + "appid=" + api_key + "&q=" + str(city)
        response = requests.get(complete_url)
        response_json = response.json()

        city_weather = {
            'city': response_json.get('name'),
            'max_temp': response_json.get('main').get('temp_max'),
            'visibility': response_json.get('visibility')/1000,
            'icon': response_json['weather'][0]['icon'],
            'description': response_json['weather'][0]['description'],
        }

        weather_data.append(city_weather)

    dict = {'weather_data': weather_data, 'form': form,
            'err_msg': err_msg, 'succ_msg': succ_msg}
    return render(request, 'backend/index.html', dict)


def delete_city(request, city_name):
    city_name = city_name.lower()
    City.objects.get(city_name=city_name).delete()
    return redirect('home')
