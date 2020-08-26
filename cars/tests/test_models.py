from django.test import TestCase

from ..models import Car


class VoteModelTestCase(TestCase):
    def setUp(self):
        self.car = Car.objects.create(make="TOYOTA", model="PREVIA")

    def test_upvote(self):
        self.car.upvote(5)
        self.car.upvote(3)
        self.assertEqual(self.car.votes, 2)
        self.assertEqual(self.car.sum_of_rates, 8)

    def test_average(self):
        self.car.upvote(5)
        self.car.upvote(2)
        self.assertEqual(self.car.average, 3.5)


class CarManagerTestCase(TestCase):
    def setUp(self):
        c1 = Car.objects.create(make="TOYOTA", model="PREVIA")
        c2 = Car.objects.create(make="PORSCHE", model="CAYENNE")
        c3 = Car.objects.create(make="DODGE", model="CARAVAN")

        # votes
        c3.upvote(7)
        c3.upvote(4)
        c3.upvote(7)
        c1.upvote(4)
        c1.upvote(5)

    def test_filter_by_popularity(self):
        popular_cars = Car.objects.filter_by_popularity()
        rates = []
        for car in popular_cars:
            rates.append(car.votes)

        self.assertEqual(rates, [3, 2, 0])
