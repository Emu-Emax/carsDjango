from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from ..models import Car

GET_POST_CARS = reverse('cars')
POST_RATE = reverse('rate')
GET_POPULARS = reverse('populars')


class CreateCarViewTest(TestCase):
    def setUp(self):
        self.c1 = Car.objects.create(make="TOYOTA", model="PREVIA")
        self.c2 = Car.objects.create(make="PORSCHE", model="CAYENNE")

    def test_get_object_list(self):
        response = self.client.get(GET_POST_CARS)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_object_success(self):
        make = 'HONDA'
        model = 'Odyssey'
        body = {
            'make': make,
            'model': model,
        }
        response = self.client.post(GET_POST_CARS, body)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        created_car = Car.objects.get(make=make, model=model)
        self.assertIn(created_car, Car.objects.all())

    def test_post_object_not_exists_in_external_API(self):
        body = {
            'make': self.c2.make,
            'model': self.c2.model,
        }
        response = self.client.post(GET_POST_CARS, body)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Car.objects.count(), 2)

    def test_post_object_no_params(self):
        body = {}
        response = self.client.post(GET_POST_CARS, body)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Car.objects.count(), 2)


class RateCarViewTest(TestCase):
    def setUp(self):
        self.car = Car.objects.create(make="TOYOTA", model="PREVIA")

    def test_vote_success(self):
        body = {
            'car_id': self.car.pk,
            'rate': 3
        }
        response = self.client.post(POST_RATE, body)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        updated_car = Car.objects.get(pk=self.car.pk)
        self.assertEqual(updated_car.votes, 1)
        self.assertEqual(updated_car.sum_of_rates, 3)

    def test_vote_no_params(self):
        body = {}
        response = self.client.post(POST_RATE, body)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_vote_wrong_params(self):
        body = {
            'car_id': 'STRING',
            'rate': 'STRING',
        }
        response = self.client.post(POST_RATE, body)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_wrong_vote_note(self):
        body = {
            'car_id': self.car.pk,
            'rate': 7,
        }
        response = self.client.post(POST_RATE, body)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_object_not_exists(self):
        body = {
            'car_id': 2,
            'rate': 5,
        }
        response = self.client.post(POST_RATE, body)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class PopularCarsView(TestCase):

    def test_get_popular_cars(self):
        self.c1 = Car.objects.create(make="TOYOTA", model="PREVIA")
        self.c2 = Car.objects.create(make="FORD", model="FOCUS")
        self.c3 = Car.objects.create(make="AUDI", model="A4")

        self.c2.upvote(3)
        self.c2.upvote(5)
        self.c3.upvote(1)

        response = self.client.get(GET_POPULARS)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_no_cars_in_db(self):
        response = self.client.get(GET_POPULARS)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        result = [r for r in response.data]
        self.assertEqual(result, [])
