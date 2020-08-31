from django.test import TestCase
from django.urls import reverse

from ..models import Car


class CreateCarViewTest(TestCase):
    def setUp(self):
        self.c1 = Car.objects.create(make="TOYOTA", model="PREVIA")
        self.c2 = Car.objects.create(make="PORSCHE", model="CAYENNE")

    def test_get_object_list(self):
        response = self.client.get(reverse('cars'))
        self.assertEqual(response.status_code, 200)

    def test_post_object_success(self):
        make = 'HONDA'
        model = 'Odyssey'
        body = {
            'make': make,
            'model': model,
        }
        response = self.client.post(reverse('cars'), body)
        self.assertEqual(response.status_code, 201)
        created_car = Car.objects.get(make=make, model=model)
        self.assertIn(created_car, Car.objects.all())

    def test_post_object_not_exists_in_external_API(self):
        body = {
            'make': self.c2.make,
            'model': self.c2.model,
        }
        response = self.client.post(reverse('cars'), body)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(Car.objects.count(), 2)

    def test_post_object_no_params(self):
        body = {}
        response = self.client.post(reverse('cars'), body)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Car.objects.count(), 2)


class RateCarViewTest(TestCase):
    def setUp(self):
        self.car = Car.objects.create(make="TOYOTA", model="PREVIA")

    def test_vote_success(self):
        body = {
            'car_id': self.car.pk,
            'rate': 3
        }
        response = self.client.post(reverse('rate'), body)
        self.assertEqual(response.status_code, 200)

        updated_car = Car.objects.get(pk=self.car.pk)
        self.assertEqual(updated_car.votes, 1)
        self.assertEqual(updated_car.sum_of_rates, 3)

    def test_vote_no_params(self):
        body = {}
        response = self.client.post(reverse('rate'), body)
        self.assertEqual(response.status_code, 400)

    def test_vote_wrong_params(self):
        body = {
            'car_id': 'STRING',
            'rate': 'STRING',
        }
        response = self.client.post(reverse('rate'), body)
        self.assertEqual(response.status_code, 400)

    def test_wrong_vote_note(self):
        body = {
            'car_id': self.car.pk,
            'rate': 7,
        }
        response = self.client.post(reverse('rate'), body)
        self.assertEqual(response.status_code, 400)

    def test_object_not_exists(self):
        body = {
            'car_id': 2,
            'rate': 5,
        }
        response = self.client.post(reverse('rate'), body)
        self.assertEqual(response.status_code, 404)


class PopularCarsView(TestCase):

    def test_get_popular_cars(self):
        self.c1 = Car.objects.create(make="TOYOTA", model="PREVIA")
        self.c2 = Car.objects.create(make="FORD", model="FOCUS")
        self.c3 = Car.objects.create(make="AUDI", model="A4")

        self.c2.upvote(3)
        self.c2.upvote(5)
        self.c3.upvote(1)

        response = self.client.get(reverse('populars'))
        self.assertEqual(response.status_code, 200)

    def test_no_cars_in_db(self):
        response = self.client.get(reverse('populars'))
        self.assertEqual(response.status_code, 200)
        result = [r for r in response.data]
        self.assertEqual(result, [])
