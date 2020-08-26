import requests
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from .models import Car


def index(request):
    return render(request, 'home.html')


def render_list_cars(request, msg, status=200):
    cars = Car.objects.all()
    context = {'cars': cars, 'message': msg}
    return render(request, 'list.html', context=context, status=status)


def render_add_template(request, msg='', status=200):
    context = {'message': msg}
    return render(request, 'add.html', context=context, status=status)


class CreateCarView(View):

    def fetch_car_makes(self):
        makes = requests.get('https://vpic.nhtsa.dot.gov/api/vehicles/getallmakes?format=json')
        makes_json = makes.json()
        return makes_json['Results']

    def fetch_car_models(self, car_make):
        models = requests.get('https://vpic.nhtsa.dot.gov/api/vehicles/getmodelsformake/' + car_make + '?format=json')
        models_json = models.json()
        return models_json['Results']

    def get(self, request):
        return render_list_cars(request, msg='')

    def post(self, request, *args, **kwargs):
        car_make = str.upper(request.POST.get('make', '')).rstrip()
        car_model = request.POST.get('model', '').rstrip()
        car_makes = self.fetch_car_makes()

        for m in car_makes:
            if car_make == m['Make_Name'].rstrip():
                car_models = self.fetch_car_models(car_make)

                for car in car_models:
                    if car['Model_Name'].rstrip() == car_model:
                        Car.objects.get_or_create(make=car_make, model=car_model)
                        return render_add_template(request, 'Database updated with new car!')

        return render_add_template(request, 'Car does not exist!', status=404)


class RateCarView(View):
    def post(self, request, *args, **kwargs):
        car_id = request.POST.get('car_id', '')
        rate = request.POST.get('rate', '')

        if not car_id.isnumeric() or not rate.isnumeric():
            return HttpResponse(status=400)

        if int(rate) not in [1, 2, 3, 4, 5]:
            return HttpResponse(status=400)

        try:
            car = Car.objects.get(pk=car_id)
            car.upvote(int(rate))
            return render_list_cars(request, msg='Voted for a car!')
        except Car.DoesNotExist:
            return render_list_cars(request, msg='Car does not exist!', status=404)


class PopularCarsView(View):
    def get(self, request):
        cars = Car.objects.filter_by_popularity()
        return render(request, 'populars.html', context={'cars': cars})
