import requests
import time
import json
from django.shortcuts import render, redirect
from .models import City
from .forms import CityForm

def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&APPID=4c87e57040ad2db49809e87db3046642'
    
    cities = City.objects.all()

    if request.method == 'POST':
        for city in cities:
            if city.name == request.POST['name']:
                return redirect('/')
        form = CityForm(request.POST)
        form.save()

    form = CityForm()
    
    weather_data = []

    for city in cities:

        r = requests.get(url.format(city.name)).json()
        print('\n')
        print(json.dumps(r, indent=4, sort_keys=False))
        print('\n\n')

        city_weather = {
            'id' : city.id,
            'city': city.name,
            'temperature': r['main']['temp'],
            'description': r['weather'][0]['description'],
            'icon': r['weather'][0]['icon'],
        }

        weather_data.append(city_weather)

    if r['cod'] == '404':
        print('11111111111111111111111111\n')
        City.objects.all().last().delete()
        context = {'wrong_city':True}
    else:
        context = {'weather_data' : weather_data[::-1], 'form' : form}
    time.sleep(1)
    return render(request, 'weather/weather.html', context)


def delete(request, id):
    print('About to delete')
    context = {
        'weather': City.objects.get(id=id).delete()
    }
    time.sleep(1)
    return redirect('/', context)
