from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Car
from .services import fetch_car_models
from .serializers import CarSerializer
from rest_framework import generics, status


def index(request):
    return render(request, 'home.html')


def render_list_cars(request, msg, status=200):
    cars = Car.objects.all()
    context = {'cars': cars, 'message': msg}
    return render(request, 'list.html', context=context, status=status)


def render_add_template(request, msg='', status=200):
    context = {'message': msg}
    return render(request, 'add.html', context=context, status=status)


class CreateCarView(APIView):

    def get(self, request):
        cars_serializer = CarSerializer(Car.objects.all(), many=True)
        return Response(cars_serializer.data)

    def post(self, request, *args, **kwargs):
        cars_serializer = CarSerializer(data=request.data)

        car_make = str.upper(request.POST.get('make', '')).rstrip()
        car_model = request.POST.get('model', '').rstrip()

        if car_make:
            car_models = fetch_car_models(car_make)

            for car in car_models:
                if car['Model_Name'].rstrip() == car_model and cars_serializer.is_valid():
                    cars_serializer.save()
                    return Response(cars_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_404_NOT_FOUND)


class RateCarView(APIView):
    def post(self, request, *args, **kwargs):
        car_id = request.POST.get('car_id', '')
        rate = request.POST.get('rate', '')

        if not car_id.isnumeric() or not rate.isnumeric():
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if int(rate) not in [1, 2, 3, 4, 5]:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            car = Car.objects.get(pk=car_id)
            car.upvote(int(rate))
            return Response('Voted for a car', status=status.HTTP_200_OK)
        except Car.DoesNotExist:
            return Response('Car not found', status=status.HTTP_404_NOT_FOUND)


class PopularCarsView(generics.ListAPIView):
    serializer_class = CarSerializer

    def get_queryset(self):
        qs = Car.objects.filter_by_popularity()
        return qs
